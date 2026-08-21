"""
Pipeline stages: extract -> hydrate -> verify -> register.
"""

import os

import accounting_client
import hydrate as hydrate_module
import llm_client
import ocr_client
import verify as verify_module

PDF_EXTENSIONS = {".pdf"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}


class UnsupportedFileType(Exception):
    pass


def extract(storage_path: str, original_filename: str) -> dict:
    """file on disk -> structured extraction.

    Orchestration: route by file type. PDFs (with or without a text layer)
    go to the LLM path; scanned images go to the OCR path. Both are mocked
    for now, returning hand-transcribed data for the 12 sample invoices,
    but the call site here is where a real LLM/OCR integration plugs in.
    """
    ext = os.path.splitext(original_filename)[1].lower()

    with open(storage_path, "rb") as f:
        file_bytes = f.read()

    if ext in PDF_EXTENSIONS:
        return llm_client.extract_from_pdf(file_bytes, original_filename)
    if ext in IMAGE_EXTENSIONS:
        return ocr_client.extract_from_image(file_bytes, original_filename)
    raise UnsupportedFileType(f"No extraction route for file type {ext!r}")


def hydrate(extracted: dict) -> tuple[dict, list[dict]]:
    """structured extraction -> (draft API payload, unresolved issues).

    Resolves supplier name -> partner_code, tax rate % -> tax_code, and
    Japanese date formats -> YYYY-MM-DD against the accounting API's own
    reference data (GET /partners). Never rejects anything itself -- it
    just reports what it couldn't map; verify() decides what's fatal.
    """
    partners = accounting_client.get_partners()
    return hydrate_module.hydrate(extracted, partners)


def verify(payload: dict, hydration_issues: list[dict], db_session) -> dict:
    """draft payload -> {"ok": bool, "issues": [...], "payload": {...} | None}

    `payload` is only returned when ok -- everything resolved, math
    reconciles, and no duplicate found locally.
    """
    return verify_module.verify(payload, hydration_issues, db_session)


def register(payload: dict) -> dict:
    """API-shaped payload -> {"success": bool, "data": ..., "error": ...}"""
    raise NotImplementedError
