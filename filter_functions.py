from __future__ import annotations

import re


def validate_phone_number(phone_number: str) -> bool:
    if not phone_number or not any(ch.isdigit() for ch in phone_number) or any(ch.isalpha() for ch in phone_number):
        return False
    phone_number: str = str(int("".join(ch for ch in phone_number if ch.isdigit())))
    pattern = re.compile(r"/^([\+]+)*[0-9\x20\x28\x29\-]{5,20}$/")
    return True if re.search(pattern, phone_number) and len(phone_number) <= 13 else False
