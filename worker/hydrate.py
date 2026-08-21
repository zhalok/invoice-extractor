"""
Hydration: raw extraction -> draft API payload.

Resolves everything the accounting API needs an ID/code for, since the
extractor only ever sees what's printed on the invoice:
  - supplier name (as printed, possibly an alias) -> partner_code
  - tax rate in %                                 -> tax_code
  - Japanese date formats (kanji, slashes, Reiwa)  -> YYYY-MM-DD

Returns (payload, issues). `payload` is always returned, even partially
filled, so verify() and a future human-review UI can show what's known;
`issues` lists anything that could not be resolved. verify() decides
whether unresolved issues block registration -- hydration itself doesn't
reject anything, it just reports what it could not map.
"""

import re

TAX_RATE_TO_CODE = {10: "T10", 8: "T08"}

_KANJI_DATE = re.compile(r"^(\d{4})年(\d{1,2})月(\d{1,2})日$")
_SLASH_DATE = re.compile(r"^(\d{4})/(\d{1,2})/(\d{1,2})$")
_REIWA_DATE = re.compile(r"^令和(\d{1,2})年(\d{1,2})月(\d{1,2})日$")
REIWA_EPOCH_YEAR = 2018  # 令和1年 = 2019, so 令和N年 = 2018 + N


def normalize_date(raw: str) -> str | None:
    """Return YYYY-MM-DD, or None if the format isn't recognized."""
    if m := _KANJI_DATE.match(raw):
        year, month, day = m.groups()
    elif m := _SLASH_DATE.match(raw):
        year, month, day = m.groups()
    elif m := _REIWA_DATE.match(raw):
        reiwa_year, month, day = m.groups()
        year = str(REIWA_EPOCH_YEAR + int(reiwa_year))
    else:
        return None
    return f"{int(year):04d}-{int(month):02d}-{int(day):02d}"


def resolve_partner_code(supplier_name_raw: str, partners: list[dict]) -> str | None:
    """Exact match against each partner's registered name or aliases."""
    name = supplier_name_raw.strip()
    for partner in partners:
        if name == partner["name"]:
            return partner["partner_code"]
        if name in partner.get("aliases", []):
            return partner["partner_code"]
    return None


def hydrate(extracted: dict, partners: list[dict]) -> tuple[dict, list[dict]]:
    issues = []

    partner_code = resolve_partner_code(extracted["supplier_name_raw"], partners)
    if partner_code is None:
        issues.append({
            "code": "PARTNER_NOT_RESOLVED",
            "message": f"Supplier name {extracted['supplier_name_raw']!r} does not match any "
                       f"partner name or alias in the partner master.",
        })

    issue_date = normalize_date(extracted["issue_date_raw"])
    if issue_date is None:
        issues.append({
            "code": "DATE_NOT_RESOLVED",
            "message": f"issue_date {extracted['issue_date_raw']!r} did not match any known date format.",
        })

    due_date = normalize_date(extracted["due_date_raw"])
    if due_date is None:
        issues.append({
            "code": "DATE_NOT_RESOLVED",
            "message": f"due_date {extracted['due_date_raw']!r} did not match any known date format.",
        })

    lines = []
    for i, line in enumerate(extracted["lines"]):
        tax_code = TAX_RATE_TO_CODE.get(line["tax_rate"])
        if tax_code is None:
            issues.append({
                "code": "TAX_RATE_NOT_RESOLVED",
                "message": f"lines[{i}] has tax_rate {line['tax_rate']!r}, no known tax_code for it.",
            })
        lines.append({
            "description": line["description"],
            "quantity": line["quantity"],
            "unit": line["unit"],
            "unit_price": line["unit_price"],
            "amount": line["amount"],
            "tax_code": tax_code,
        })

    payload = {
        "partner_code": partner_code,
        "invoice_number": extracted["invoice_number"],
        "issue_date": issue_date,
        "due_date": due_date,
        "currency": "JPY",
        "lines": lines,
        "subtotal": extracted["subtotal"],
        "tax_amount": extracted["tax_amount"],
        "total_amount": extracted["total_amount"],
    }
    return payload, issues
