def to_brl(value: float) -> str:
    """Formats a float value as a Brazilian Real currency string."""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
