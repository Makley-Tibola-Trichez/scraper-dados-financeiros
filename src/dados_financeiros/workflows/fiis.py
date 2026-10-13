from sqlite3 import Connection
from typing import cast

from gspread import Cell, Client
from gspread.utils import ValueInputOption
from playwright.sync_api import Page

from dados_financeiros.utils.formatters import to_br_decimal
from dados_financeiros.utils.progresso_processo import ProgressoProcessos

from ..config.config import Config
from ..fii.application.salvar_dados_fiis_use_case import SalvarFiiUseCase
from ..fii.domain.value_objects import Fii
from ..fii.infrastructure.fii_investidor10_gateway import FiiInvestidor10Gateway
from ..fii.infrastructure.fii_repository import FiiRepository
from ..sheet.cell_builder import build_cells
from ..sheet.fiis_cols import FiisCols
from ..utils.logger import logger


def scrapper_fiis(gc: Client, spreadsheet_id: str, page: Page, conn: Connection) -> None:
    sheet = gc.open_by_key(spreadsheet_id).get_worksheet_by_id(Config.id_worksheet_fiis_base)
    tickers_existentes = cast(list[str], sheet.col_values(1))
    # tickers_existentes = list(set(tickers_existentes).difference(set(LISTA_DE_TICKERS_EXCLUSAO)))
    # tickers_existentes.sort()

    fii_repository = FiiRepository(conn, logger=logger)
    pagina_fii_gateway = FiiInvestidor10Gateway(page, logger)
    salvar_fii_use_case = SalvarFiiUseCase(logger, pagina_fii_gateway, fii_repository)

    fiis: list[Fii] = salvar_fii_use_case.executar(tickers_existentes[1:])

    processo_atualizacao_planilhas_fiis = ProgressoProcessos(
        total_processos=len(fiis),
        descricao_tipo_processo="Atualização de Planilha de FIIs",
    )
    cells_to_update: list[Cell] = []
    for i, fii in enumerate(fiis):
        processo_atualizacao_planilhas_fiis.atualizar_progresso(nome_processo=fii.ticker, indice_processo=i + 1)
        if fii.ticker not in tickers_existentes:
            continue
        logger.info(f"{fii.ticker}, gerando células com novos valores")
        linha = tickers_existentes.index(fii.ticker) + 1

        valores: list[tuple[FiisCols, str | None]] = [
            (FiisCols.TIPO_DE_FUNDO, fii.tipo_de_fundo),
            (FiisCols.SEGMENTO, fii.segmento),
            (FiisCols.COTACAO, to_br_decimal(fii.cotacao)),
            (FiisCols.PVP, fii.pvp),
            (FiisCols.DIVDENDO_1M, fii.dividendo_1_mes),
            (FiisCols.DIVIDENDO_3M, fii.dividendo_3_meses),
            (FiisCols.DIVIDENDO_6M, fii.dividendo_6_meses),
            (FiisCols.DIVIDENDO_12M, fii.dividendo_12_meses),
            (FiisCols.DY_1M, fii.dividend_yield_1_mes),
            (FiisCols.DY_3M, fii.dividend_yield_3_meses),
            (FiisCols.DY_6M, fii.dividend_yield_6_meses),
            (FiisCols.DY_12M, fii.dividend_yield_12_meses),
            (FiisCols.QUANTIDADE_COTAS, fii.quantidade_cotas_emitidas),
            (FiisCols.VALOR_PATRIMONIAL_POR_COTA, fii.valor_patrimonial_por_cota),
        ]

        cells_to_update.extend(build_cells(linha, valores))

    if not cells_to_update:
        logger.warning("Nenhuma célula para atualizar (nenhum FII processado com sucesso)")
        return

    logger.info("Atualizando planilha")
    sheet.update_cells(cells_to_update, value_input_option=ValueInputOption.user_entered)
    logger.info("Planilha atualizada")
