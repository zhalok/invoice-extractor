"""
Mock LLM client for PDFs with a text layer.

Stands in for a real call to a vision/document-capable LLM (e.g. Claude)
given the PDF bytes plus an extraction prompt asking for the schema below.
Swapping this for a real implementation means replacing the body of
extract_from_pdf() with an API call, keeping the same return shape.
"""

from mock_data import INVOICES


class ExtractionError(Exception):
    pass


def extract_from_pdf(file_bytes: bytes, original_filename: str) -> dict:
    data = INVOICES.get(original_filename)
    if data is None:
        raise ExtractionError(f"LLM mock has no data for {original_filename!r}")
    return {"source": "llm", **data}
