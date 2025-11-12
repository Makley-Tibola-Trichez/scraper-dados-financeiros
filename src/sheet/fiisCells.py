from enum import Enum
from gspread.cell import Cell


class FiisCols(Enum):
    TICKER = 1
    SETOR = TICKER + 1
    SEGMENTO = SETOR + 1
    COTACAO = SEGMENTO + 1
    PL = COTACAO + 1
    PVP = PL + 1
    DIVIDEND_YIELD = PVP + 1
    PAYOUT = DIVIDEND_YIELD + 1
    MEDIA_DIVIDENDOS_12_MESES = PAYOUT + 1
    EFEITO_BOLA_DE_NEVE = MEDIA_DIVIDENDOS_12_MESES + 1
    DIVIDENDO_ANUAL_2025 = EFEITO_BOLA_DE_NEVE + 1
    DIVIDENDO_ANUAL_2024 = DIVIDENDO_ANUAL_2025 + 1
    DIVIDENDO_ANUAL_2023 = DIVIDENDO_ANUAL_2024 + 1
    DIVIDENDO_ANUAL_2022 = DIVIDENDO_ANUAL_2023 + 1
    PRECO_TETO_BAZIN = DIVIDENDO_ANUAL_2022 + 1
    CAGR_RECEITAS_5_ANOS = PRECO_TETO_BAZIN + 1
    CAGR_LUCROS_5_ANOS = CAGR_RECEITAS_5_ANOS + 1
    DIVIDA_LIQUIDA_SOBRE_PATRIMONIO = CAGR_LUCROS_5_ANOS + 1
    
class FiisCells:
    def __init__(self, row: int):
        self.row = row

    def _make_cell(self, col_enum, value: str | None, force_update: bool = False) -> Cell | None:
        if force_update or value is not None:
            return Cell(self.row, col_enum.value, value)
        return None

    def cell_cotacao(self, value: str | None, force_update: bool = False) -> Cell | None:
        return self._make_cell(FiisCols.COTACAO, value, force_update)

    def cell_pl(self, value: str | None, force_update: bool = False) -> Cell | None:
        return self._make_cell(FiisCols.PL, value, force_update)

    def cell_pvp(self, value: str | None, force_update: bool = False) -> Cell | None:
        return self._make_cell(FiisCols.PVP, value, force_update)
    
    def cell_dividend_yield(self, value: str | None, force_update: bool = False) -> Cell | None:
        return self._make_cell(FiisCols.DIVIDEND_YIELD, value, force_update)

    def cell_payout(self, value: str | None, force_update: bool = False) -> Cell | None:
        return self._make_cell(FiisCols.PAYOUT, value, force_update)

    def cells_dividendos(self, values: list[str], force_update: bool = False) -> list[Cell]:
        start_col = FiisCols.DIVIDENDO_ANUAL_2025.value
        return [
            Cell(self.row, start_col + i, value)
            for i, value in enumerate(values)
            if force_update or value is not None
        ]
