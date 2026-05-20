"""Buyurtma: karta (Luhn), muddat; pasport / ID formatlari — pul yechilmaydi, faqat tekshiruv."""
from __future__ import annotations

import re
from datetime import datetime


def luhn_valid(card_number: str) -> bool:
    digits = [int(c) for c in card_number if c.isdigit()]
    if len(digits) not in (13, 15, 16, 19):
        return False
    s = 0
    alt = False
    for d in reversed(digits):
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        s += d
        alt = not alt
    return s % 10 == 0


def card_brand_ok(card_number: str) -> bool:
    """Visa, Mastercard diapazonlari, UnionPay, Humo/Uzcard tipik BIN."""
    d = "".join(c for c in card_number if c.isdigit())
    if len(d) < 13:
        return False
    if d.startswith("4"):
        return True
    if len(d) >= 2:
        p2 = int(d[:2])
        if 51 <= p2 <= 55:
            return True
    if len(d) >= 4:
        p4 = int(d[:4])
        if 2221 <= p4 <= 2720:
            return True
    if d.startswith("62"):
        return True
    if d.startswith("9860") or d.startswith("8600"):
        return True
    return False


def expiry_ok(mm_yy: str) -> bool:
    m = re.match(r"^(\d{2})/(\d{2})$", (mm_yy or "").strip())
    if not m:
        return False
    month, year = int(m.group(1)), int(m.group(2))
    if not (1 <= month <= 12):
        return False
    full_year = 2000 + year
    now = datetime.now()
    exp_end = datetime(full_year, month, 1)
    return exp_end >= datetime(now.year, now.month, 1)


def uz_passport_series_number_ok(value: str) -> bool:
    """Pasport seriya va raqam: AA1234567."""
    v = (value or "").strip().upper().replace(" ", "")
    return bool(re.match(r"^[A-Z]{2}\d{7}$", v))


def uz_id_card_ok(value: str) -> bool:
    """ID karta: vaqtinchalik — 9 raqam yoki AA1234567."""
    v = (value or "").strip().upper().replace(" ", "")
    if re.match(r"^[A-Z]{2}\d{7}$", v):
        return True
    if re.match(r"^\d{9}$", v):
        return True
    return False
