"""
Pipeline stages: extract -> verify -> register.
"""

import os

import llm_client
import ocr_client

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
    # ext = os.path.splitext(original_filename)[1].lower()

    # with open(storage_path, "rb") as f:
    #     file_bytes = f.read()

    # if ext in PDF_EXTENSIONS:
    #     return llm_client.extract_from_pdf(file_bytes, original_filename)
    # if ext in IMAGE_EXTENSIONS:
    #     return ocr_client.extract_from_image(file_bytes, original_filename)
    # raise UnsupportedFileType(f"No extraction route for file type {ext!r}")
    raise NotImplementedError



def verify(extracted: dict, db_session) -> dict:
    """extraction -> {"ok": bool, "issues": [...], "payload": {...} | None}

    `payload` is the API-shaped body (partner_code resolved, tax_code per
    line, YYYY-MM-DD dates) ready for POST /invoices, present only when ok.
    """
    raise NotImplementedError


def register(payload: dict) -> dict:
    """API-shaped payload -> {"success": bool, "data": ..., "error": ...}"""
    raise NotImplementedError
