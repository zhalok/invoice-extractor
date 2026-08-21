"""
Verification: draft API payload -> ok/issues, before it ever reaches the
accounting API.

Two checks, both aimed at catching problems the accounting system would
otherwise reject (or, in the duplicate case, silently double-pay):

  - amount reconciliation, mirroring the accounting API's own recompute
    logic exactly (accounting-api/accounting_api.py: per-tax-code subtotal,
    floor the tax, sum). Catches supplier-side arithmetic errors before a
    wasted round trip.
  - duplicate detection against invoices we've already processed
    successfully (our own job history) and against what's already
    registered in the accounting system itself -- the direct fix for the
    client's near-double-payment incident.

Hydration issues (unresolved partner/date/tax_code) are folded in as
blocking: we never submit a payload with a guessed partner_code or a
malformed date.
"""

import math

import accounting_client
from models import Job

TAX_RATES = {"T10": 0.10, "T08": 0.08}


def check_amounts(payload: dict) -> list[dict]:
    issues = []
    lines = payload["lines"]

    expected_subtotal = sum(line["amount"] for line in lines)
    if payload["subtotal"] != expected_subtotal:
        issues.append({
            "code": "SUBTOTAL_MISMATCH",
            "message": f"subtotal {payload['subtotal']} does not equal the sum of line amounts "
                       f"({expected_subtotal}).",
        })

    subtotal_by_code: dict[str, int] = {}
    for line in lines:
        code = line["tax_code"]
        if code not in TAX_RATES:
            continue  # already reported as a hydration issue
        subtotal_by_code[code] = subtotal_by_code.get(code, 0) + line["amount"]

    tax_by_code = {code: math.floor(subtotal * TAX_RATES[code]) for code, subtotal in subtotal_by_code.items()}
    expected_tax = sum(tax_by_code.values())
    if payload["tax_amount"] != expected_tax:
        issues.append({
            "code": "TAX_MISMATCH",
            "message": f"tax_amount {payload['tax_amount']} does not equal the tax recalculated per tax code "
                       f"({expected_tax}, breakdown {tax_by_code}).",
        })

    expected_total = expected_subtotal + expected_tax
    if payload["total_amount"] != expected_total:
        issues.append({
            "code": "TOTAL_MISMATCH",
            "message": f"total_amount {payload['total_amount']} does not equal subtotal + tax "
                       f"({expected_total}).",
        })

    return issues


def check_duplicate(payload: dict, db_session) -> list[dict]:
    issues = []
    invoice_number = payload["invoice_number"]
    partner_code = payload["partner_code"]

    prior_job = (
        db_session.query(Job)
        .filter(
            Job.status == "done",
            Job.hydration["payload"]["invoice_number"].astext == invoice_number,
            Job.hydration["payload"]["partner_code"].astext == partner_code,
        )
        .first()
    )
    if prior_job is not None:
        issues.append({
            "code": "DUPLICATE_IN_JOB_HISTORY",
            "message": f"Invoice {invoice_number!r} for partner {partner_code!r} was already processed "
                       f"successfully by job {prior_job.id}.",
        })

    registered = accounting_client.get_invoices()
    if any(r["invoice_number"] == invoice_number and r["partner_code"] == partner_code for r in registered):
        issues.append({
            "code": "DUPLICATE_IN_ACCOUNTING_SYSTEM",
            "message": f"Invoice {invoice_number!r} for partner {partner_code!r} is already registered "
                       f"in the accounting system.",
        })

    return issues


def verify(payload: dict, hydration_issues: list[dict], db_session) -> dict:
    issues = list(hydration_issues)

    # Amount/duplicate checks need a fully resolved payload -- skip them if
    # hydration already failed, since e.g. an unresolved partner_code makes
    # a duplicate check meaningless.
    if not hydration_issues:
        issues += check_amounts(payload)
        issues += check_duplicate(payload, db_session)

    ok = len(issues) == 0
    return {"ok": ok, "issues": issues, "payload": payload if ok else None}
