"""
Mock OCR client for scanned image invoices (jpg/png).

Stands in for a real OCR + extraction pass over a scanned/handwritten
invoice image. Swapping this for a real implementation means replacing the
body of extract_from_image() with an OCR call, keeping the same return
shape.
"""

from mock_data import INVOICES


class ExtractionError(Exception):
    pass


def extract_from_image(file_bytes: bytes, original_filename: str) -> dict:
    data = INVOICES.get(original_filename)
    if data is None:
        raise ExtractionError(f"OCR mock has no data for {original_filename!r}")
    return {"source": "ocr", **data}
