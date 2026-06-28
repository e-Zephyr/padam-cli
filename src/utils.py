import re
from src.constant import JUNK_TITLES

def is_valid(text: str, href: str) -> bool:
    if href in {"/", "#"}:
        return False

    if re.fullmatch(r"[A-Z]", text):
        return False

    if re.fullmatch(r"\d+", text):
        return False

    if re.fullmatch(r"Tamil \d{4} Movies", text):
        return False

    if text in JUNK_TITLES:
        return False

    return True