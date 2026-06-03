def to_brl(value: float) -> str:
    """Formats a float value as a Brazilian Real currency string."""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def from_brl(v: str) -> str:
    return v.strip().replace("R$ ", "").replace(",", ".")


def to_br_decimal(v: float) -> str:
    return str(v).replace(".", ",")
