from enum import Enum

from gspread.cell import Cell


class AcaoCols(Enum):
    TICKER = 1
    SETOR = TICKER + 1
    SEGMENTO = SETOR + 1
    COTACAO = SEGMENTO + 1
    PL = COTACAO + 1
    PVP = PL + 1
    VPA = PVP + 1
    LPA = VPA + 1
    ROE = LPA + 1
    DIVIDEND_YIELD = ROE + 1
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


class AcaoCells:
    def __init__(self, row: int) -> None:
        self.row = row

    def __make_cell(
        self, col_enum: Enum, value: str | None, force_update: bool = False
    ) -> Cell | None:
        if force_update or value is not None:
            return Cell(self.row, col_enum.value, value)
        return None

    def cell_cotacao(
        self, value: str | None, force_update: bool = False
    ) -> Cell | None:
        return self.__make_cell(AcaoCols.COTACAO, value, force_update)

    def cell_pl(self, value: str | None, force_update: bool = False) -> Cell | None:
        return self.__make_cell(AcaoCols.PL, value, force_update)

    def cell_pvp(self, value: str | None, force_update: bool = False) -> Cell | None:
        return self.__make_cell(AcaoCols.PVP, value, force_update)

    def cell_vpa(self, value: str | None, force_update: bool = False) -> Cell | None:
        return self.__make_cell(AcaoCols.VPA, value, force_update)

    def cell_lpa(self, value: str | None, force_update: bool = False) -> Cell | None:
        return self.__make_cell(AcaoCols.LPA, value, force_update)

    def cell_roe(self, value: str | None, force_update: bool = False) -> Cell | None:
        return self.__make_cell(AcaoCols.ROE, value, force_update)

    def cell_dividend_yield(
        self, value: str | None, force_update: bool = False
    ) -> Cell | None:
        return self.__make_cell(AcaoCols.DIVIDEND_YIELD, value, force_update)

    def cell_payout(self, value: str | None, force_update: bool = False) -> Cell | None:
        return self.__make_cell(AcaoCols.PAYOUT, value, force_update)

    def cells_dividendos(
        self, values: list[str], force_update: bool = False
    ) -> list[Cell]:
        start_col = AcaoCols.DIVIDENDO_ANUAL_2025.value
        return [
            Cell(self.row, start_col + i, value)
            for i, value in enumerate(values)
            if force_update or value is not None
        ]

    def cell_setor(self, value: str | None, force_update: bool = False) -> Cell | None:
        return self.__make_cell(AcaoCols.SETOR, value, force_update)

    def cell_segmento_do_certo(
        self, value: str | None, force_update: bool = False
    ) -> Cell | None:
        return self.__make_cell(AcaoCols.SEGMENTO, value, force_update)

    def cell_media_dividendos_12_meses(
        self, value: str | None, force_update: bool = False
    ) -> Cell | None:
        return self.__make_cell(AcaoCols.MEDIA_DIVIDENDOS_12_MESES, value, force_update)
