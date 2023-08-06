from typing import Optional


def format_quotes(value: str, quote_char: Optional[str] = '"') -> str:
    return f"{quote_char}{value}{quote_char}"
