"""Thin HTTP client for the mock accounting API."""

import os

import httpx

BASE_URL = os.environ["ACCOUNTING_API_URL"]
API_KEY = os.environ["ACCOUNTING_API_KEY"]
HEADERS = {"X-API-Key": API_KEY}


def get_partners() -> list[dict]:
    resp = httpx.get(f"{BASE_URL}/partners", headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json()["data"]["partners"]


def get_tax_codes() -> list[dict]:
    resp = httpx.get(f"{BASE_URL}/tax-codes", headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json()["data"]["tax_codes"]


def register_invoice(payload: dict) -> dict:
    resp = httpx.post(f"{BASE_URL}/invoices", headers=HEADERS, json=payload, timeout=10)
    return resp.json()
