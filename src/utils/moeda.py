import re
from decimal import Decimal


def converter_valor_nomeado_para_numero(valor_str: str) -> Decimal:
    valor_str = valor_str.lower()

    # Remove símbolos e palavras desnecessárias
    valor_str = valor_str.replace("r$", "").strip()

    multiplicadores = {
        "mil": Decimal("1e3"),
        "milhão": Decimal("1e6"),
        "milhões": Decimal("1e6"),
        "bilhão": Decimal("1e9"),
        "bilhões": Decimal("1e9"),
        "trilhão": Decimal("1e12"),
        "trilhões": Decimal("1e12"),
    }

    # Extrai número (aceita vírgula ou ponto)
    numero_match = re.search(r"[\d.,]+", valor_str)
    if not numero_match:
        raise ValueError("Valor numérico não encontrado")

    numero = numero_match.group()
    numero = numero.replace(".", "").replace(",", ".") if "," in numero else numero
    numero = Decimal(numero)

    # Detecta multiplicador
    multiplicador = Decimal("1")
    for unidade, mult in multiplicadores.items():
        if unidade in valor_str:
            multiplicador = mult
            break

    return numero * multiplicador
