"""
Hand-transcribed ground truth for the 12 sample invoices.

Stands in for what a real LLM (PDFs) or OCR (images) call would return.
Keyed by original filename since that's what identifies which sample this
is; the pipeline's storage_path is a job-scoped UUID and carries no info
about which invoice it is.
"""

INVOICES = {
    "invoice_01.pdf": {
        "supplier_name_raw": "株式会社山田製作所",
        "invoice_number": "YM-2026-0107",
        "issue_date_raw": "2026年1月7日",
        "due_date_raw": "2026年2月28日",
        "lines": [
            {"description": "精密部品A-100", "quantity": 120, "unit": "個", "unit_price": 1250, "amount": 150000, "tax_rate": 10},
            {"description": "精密部品B-220", "quantity": 40, "unit": "個", "unit_price": 3400, "amount": 136000, "tax_rate": 10},
            {"description": "梱包・輸送費", "quantity": None, "unit": "式", "unit_price": None, "amount": 18000, "tax_rate": 10},
        ],
        "subtotal": 304000,
        "tax_amount": 30400,
        "total_amount": 334400,
        "confidence": 0.97,
        "notes": "Clean text-layer PDF.",
    },
    "invoice_02.pdf": {
        "supplier_name_raw": "大阪機械工業株式会社",
        "invoice_number": "OSK-26-0112",
        "issue_date_raw": "2026年1月12日",
        "due_date_raw": "2026年2月20日",
        "lines": [
            {"description": f"治具部材 No.{n:03d}", "quantity": q, "unit": "個", "unit_price": p, "amount": q * p, "tax_rate": 10}
            for n, q, p in [
                (1, 6, 930), (2, 7, 1060), (3, 8, 1190), (4, 9, 1320), (5, 10, 1450),
                (6, 11, 1580), (7, 12, 1710), (8, 13, 1840), (9, 14, 1970), (10, 15, 2100),
                (11, 16, 2230), (12, 17, 2360), (13, 18, 2490), (14, 19, 2620), (15, 20, 2750),
                (16, 21, 2880), (17, 22, 3010), (18, 23, 3140), (19, 24, 3270), (20, 25, 3400),
                (21, 26, 3530), (22, 27, 3660), (23, 28, 3790), (24, 29, 3920), (25, 30, 4050),
                (26, 31, 4180),
            ]
        ],
        "subtotal": 1419080,
        "tax_amount": 141908,
        "total_amount": 1560988,
        "confidence": 0.95,
        "notes": "Two-page PDF, 26 line items across a page break.",
    },
    "invoice_03.pdf": {
        "supplier_name_raw": "東京フーズ株式会社",
        "invoice_number": "TF-2026-0115",
        "issue_date_raw": "2026年1月15日",
        "due_date_raw": "2026年2月15日",
        "lines": [
            {"description": "業務用コーヒー豆 1kg", "quantity": 24, "unit": "袋", "unit_price": 2800, "amount": 67200, "tax_rate": 8},
            {"description": "紙コップ 100個入", "quantity": 30, "unit": "箱", "unit_price": 1200, "amount": 36000, "tax_rate": 10},
            {"description": "ミネラルウォーター 2L", "quantity": 48, "unit": "本", "unit_price": 180, "amount": 8640, "tax_rate": 8},
            {"description": "配送手数料", "quantity": None, "unit": "式", "unit_price": None, "amount": 3500, "tax_rate": 10},
        ],
        "subtotal": 115340,
        "tax_amount": 10017,
        "total_amount": 125357,
        "confidence": 0.94,
        "notes": "Mixed 8%/10% tax rates on one invoice.",
    },
    "invoice_04.jpg": {
        "supplier_name_raw": "有限会社佐藤商店",
        "invoice_number": "SATO-260118",
        "issue_date_raw": "2026/01/18",
        "due_date_raw": "2026/03/31",
        "lines": [
            {"description": "事務用品セット", "quantity": 15, "unit": "セット", "unit_price": 4800, "amount": 72000, "tax_rate": 10},
            {"description": "コピー用紙A4", "quantity": 60, "unit": "箱", "unit_price": 2450, "amount": 147000, "tax_rate": 10},
        ],
        "subtotal": 219000,
        "tax_amount": 21900,
        "total_amount": 240900,
        "confidence": 0.89,
        "notes": "Scanned image; stamp/handwriting '受領 1/20 経理' near the recipient block, unrelated to invoice fields.",
    },
    "invoice_05.jpg": {
        "supplier_name_raw": "みらいITソリューションズ株式会社",
        "invoice_number": "MIT-2026-011",
        "issue_date_raw": "2026年1月20日",
        "due_date_raw": "2026年2月28日",
        "lines": [
            {"description": "基幹システム保守（1月分）", "quantity": None, "unit": "式", "unit_price": None, "amount": 280000, "tax_rate": 10},
            {"description": "障害対応（時間外）", "quantity": 6, "unit": "時間", "unit_price": 12000, "amount": 72000, "tax_rate": 10},
            {"description": "VPN回線利用料", "quantity": None, "unit": "式", "unit_price": None, "amount": 45000, "tax_rate": 10},
        ],
        "subtotal": 397000,
        "tax_amount": 39700,
        "total_amount": 436700,
        "confidence": 0.93,
        "notes": "Scanned image, clean layout.",
    },
    "invoice_06.jpg": {
        "supplier_name_raw": "ヤマダ製作所",
        "invoice_number": "YM-2026-0122",
        "issue_date_raw": "2026年1月22日",
        "due_date_raw": "2026年2月28日",
        "lines": [
            {"description": "表面処理加工", "quantity": 200, "unit": "個", "unit_price": 340, "amount": 68000, "tax_rate": 10},
            {"description": "特急対応費", "quantity": None, "unit": "式", "unit_price": None, "amount": 25000, "tax_rate": 10},
        ],
        "subtotal": 93000,
        "tax_amount": 9300,
        "total_amount": 102300,
        "confidence": 0.9,
        "notes": "Supplier printed as alias 'ヤマダ製作所', not the registered legal name.",
    },
    "invoice_07.jpg": {
        "supplier_name_raw": "株式会社山田製作所",
        "invoice_number": "YM-2026-0107",
        "issue_date_raw": "2026年1月7日",
        "due_date_raw": "2026年2月28日",
        "lines": [
            {"description": "精密部品A-100", "quantity": 120, "unit": "個", "unit_price": 1250, "amount": 150000, "tax_rate": 10},
            {"description": "精密部品B-220", "quantity": 40, "unit": "個", "unit_price": 3400, "amount": 136000, "tax_rate": 10},
            {"description": "梱包・輸送費", "quantity": None, "unit": "式", "unit_price": None, "amount": 18000, "tax_rate": 10},
        ],
        "subtotal": 304000,
        "tax_amount": 30400,
        "total_amount": 334400,
        "confidence": 0.9,
        "notes": "Scanned copy — identical invoice number, supplier and amounts to invoice_01.pdf. This is the "
                 "near-duplicate-payment scenario the client described: the same invoice arriving twice.",
    },
    "invoice_08.jpg": {
        "supplier_name_raw": "東京フーズ株式会社",
        "invoice_number": "TF-2026-0125",
        "issue_date_raw": "2026年1月25日",
        "due_date_raw": "2026年2月25日",
        "lines": [
            {"description": "冷凍食材セット", "quantity": 12, "unit": "箱", "unit_price": 8600, "amount": 103200, "tax_rate": 8},
            {"description": "保冷配送料", "quantity": None, "unit": "式", "unit_price": None, "amount": 6800, "tax_rate": 10},
        ],
        "subtotal": 110000,
        "tax_amount": 8936,
        "total_amount": 118936,
        "confidence": 0.82,
        "notes": "Handwritten red-ink correction to the bank transfer account number ('...567 -> ...5 に変更') and a "
                 "handwritten '至急' (urgent) note. Neither field is part of the accounting API schema, so it does "
                 "not affect registration, but a human reviewer should see it.",
    },
    "invoice_09.pdf": {
        "supplier_name_raw": "大阪機械工業株式会社",
        "invoice_number": "OSK-26-0128",
        "issue_date_raw": "2026年1月28日",
        "due_date_raw": "2026年2月20日",
        "lines": [
            {"description": "シャフト加工", "quantity": 37, "unit": "個", "unit_price": 2733, "amount": 101121, "tax_rate": 10},
            {"description": "熱処理", "quantity": 37, "unit": "個", "unit_price": 891, "amount": 32967, "tax_rate": 10},
        ],
        "subtotal": 134088,
        "tax_amount": 13408,
        "total_amount": 147497,
        "confidence": 0.86,
        "notes": "PDF with no text layer (scanned image inside a PDF container). The printed total (147,497) is 1 yen "
                 "off from subtotal + tax as printed on the document (134,088 + 13,408 = 147,496) -- this looks like "
                 "a rounding error on the supplier's own document, not a reading error.",
    },
    "invoice_10.jpg": {
        "supplier_name_raw": "新星ロジスティクス株式会社",
        "invoice_number": "SSL-2026-0203",
        "issue_date_raw": "2026年2月3日",
        "due_date_raw": "2026年3月31日",
        "lines": [
            {"description": "倉庫保管料（1月分）", "quantity": None, "unit": "式", "unit_price": None, "amount": 120000, "tax_rate": 10},
            {"description": "入出庫作業", "quantity": 340, "unit": "件", "unit_price": 220, "amount": 74800, "tax_rate": 10},
        ],
        "subtotal": 194800,
        "tax_amount": 19480,
        "total_amount": 214280,
        "confidence": 0.92,
        "notes": "Supplier '新星ロジスティクス株式会社' does not appear in the partner master or its aliases.",
    },
    "invoice_11.jpg": {
        "supplier_name_raw": "有限会社佐藤商店",
        "invoice_number": "SATO-260205",
        "issue_date_raw": "令和8年2月5日",
        "due_date_raw": "令和8年3月31日",
        "lines": [
            {"description": "清掃用品一式", "quantity": None, "unit": "式", "unit_price": None, "amount": 34500, "tax_rate": 10},
            {"description": "トイレットペーパー", "quantity": 40, "unit": "箱", "unit_price": 1980, "amount": 79200, "tax_rate": 10},
        ],
        "subtotal": 113700,
        "tax_amount": 11370,
        "total_amount": 125070,
        "confidence": 0.88,
        "notes": "Dates given in the Japanese Reiwa era (令和8年 = 2026) rather than the Gregorian calendar.",
    },
    "invoice_12.jpg": {
        "supplier_name_raw": "みらいITソリューションズ株式会社",
        "invoice_number": "MIT-2026-014",
        "issue_date_raw": "2026年2月10日",
        "due_date_raw": "2026年3月31日",
        "lines": [
            {"description": "業務システム改修", "quantity": None, "unit": "式", "unit_price": None, "amount": 450000, "tax_rate": 10},
            {"description": "追加ライセンス", "quantity": 5, "unit": "本", "unit_price": 24000, "amount": 120000, "tax_rate": 10},
            {"description": "値引き", "quantity": None, "unit": "式", "unit_price": None, "amount": -30000, "tax_rate": 10},
        ],
        "subtotal": 540000,
        "tax_amount": 54000,
        "total_amount": 594000,
        "confidence": 0.91,
        "notes": "Contains a negative line item (discount, △30,000).",
    },
}
