from enum import Enum

from gspread.cell import Cell


class FiisCols(Enum):
    TICKER = 1
    TIPO_DE_FUNDO = TICKER + 1
    SEGMENTO = TIPO_DE_FUNDO + 1
    COTACAO = SEGMENTO + 1
    PVP = COTACAO + 1
    EFEITO_BOLA_DE_NEVE = PVP + 1
    DIVDENDO_1M = EFEITO_BOLA_DE_NEVE + 1
    DIVIDENDO_3M = DIVDENDO_1M + 1
    DIVIDENDO_6M = DIVIDENDO_3M + 1
    DIVIDENDO_12M = DIVIDENDO_6M + 1
    DY_1M = DIVIDENDO_12M + 1
    DY_3M = DY_1M + 1
    DY_6M = DY_3M + 1
    DY_12M = DY_6M + 1
    QUANTIDADE_COTAS = DY_12M + 1
    VALOR_PATRIMONIAL_POR_COTA = QUANTIDADE_COTAS + 1


class FiisCells:
    def __init__(self, row: int) -> None:
        self.row = row

    def make_cell(
        self,
        col_enum: FiisCols,
        value: str | None,
    ) -> Cell | None:
        if value is not None:
            return self.make_cell_trusted(col_enum, value)
        return None

    def make_cell_trusted(self, col_enum: FiisCols, value: str):
        return Cell(self.row, col_enum.value, value)
