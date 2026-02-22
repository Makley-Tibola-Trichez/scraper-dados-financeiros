from sqlite3 import Connection
from typing import cast

from gspread import Cell, Client
from gspread.utils import ValueInputOption

from dados_financeiros.utils.progresso_processo import ProgressoProcessos

from ..config.config import Config
from ..fii.application.salvar_dados_fiis_use_case import SalvarFiiUseCase
from ..fii.domain.value_objects import Fii
from ..fii.infrastructure.fii_investidor10_gateway import FiiInvestidor10Gateway
from ..fii.infrastructure.fii_repository import FiiRepository
from ..sheet.fiis_cells import FiisCells, FiisCols
from ..utils.logger import logger
from ..utils.webdriver import WebDriver


def scrapper_fiis(gc: Client, spreadsheet_id: str, driver: WebDriver, conn: Connection) -> None:  # noqa: C901
    sheet = gc.open_by_key(spreadsheet_id).get_worksheet_by_id(Config.id_worksheet_fiis_base)
    tickers_existentes = cast(list[str], sheet.col_values(1))

    fii_repository = FiiRepository(conn, logger=logger)
    pagina_fii_gateway = FiiInvestidor10Gateway(driver, logger)
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

        fii_cells = FiisCells(linha)

        tipo_de_fundo = fii_cells.make_cell(FiisCols.TIPO_DE_FUNDO, fii.tipo_de_fundo)
        if tipo_de_fundo:
            cells_to_update.append(tipo_de_fundo)

        segmento = fii_cells.make_cell(FiisCols.SEGMENTO, fii.segmento)
        if segmento:
            cells_to_update.append(segmento)

        cotacao = fii_cells.make_cell(FiisCols.COTACAO, fii.cotacao)
        if cotacao:
            cells_to_update.append(cotacao)

        pvp = fii_cells.make_cell(FiisCols.PVP, fii.pvp)
        if pvp:
            cells_to_update.append(pvp)

        dividendo_1m = fii_cells.make_cell(FiisCols.DIVDENDO_1M, fii.dividendo_1_mes)
        if dividendo_1m:
            cells_to_update.append(dividendo_1m)

        dividendo_3m = fii_cells.make_cell(FiisCols.DIVIDENDO_3M, fii.dividendo_3_meses)
        if dividendo_3m:
            cells_to_update.append(dividendo_3m)

        dividendo_6m = fii_cells.make_cell(FiisCols.DIVIDENDO_6M, fii.dividendo_6_meses)
        if dividendo_6m:
            cells_to_update.append(dividendo_6m)

        dividendo_12m = fii_cells.make_cell(FiisCols.DIVIDENDO_12M, fii.dividendo_12_meses)
        if dividendo_12m:
            cells_to_update.append(dividendo_12m)

        dy_1m = fii_cells.make_cell(FiisCols.DY_1M, fii.dividend_yield_1_mes)
        if dy_1m:
            cells_to_update.append(dy_1m)

        dy_3m = fii_cells.make_cell(FiisCols.DY_3M, fii.dividend_yield_3_meses)
        if dy_3m:
            cells_to_update.append(dy_3m)

        dy_6m = fii_cells.make_cell(FiisCols.DY_6M, fii.dividend_yield_6_meses)
        if dy_6m:
            cells_to_update.append(dy_6m)

        dy_12m = fii_cells.make_cell(FiisCols.DY_12M, fii.dividend_yield_12_meses)
        if dy_12m:
            cells_to_update.append(dy_12m)

        quantidade_cotas = fii_cells.make_cell(FiisCols.QUANTIDADE_COTAS, fii.quantidade_cotas_emitidas)
        if quantidade_cotas:
            cells_to_update.append(quantidade_cotas)

        valor_patrimonial_por_cota = fii_cells.make_cell(
            FiisCols.VALOR_PATRIMONIAL_POR_COTA, fii.valor_patrimonial_por_cota
        )
        if valor_patrimonial_por_cota:
            cells_to_update.append(valor_patrimonial_por_cota)
    logger.info("Atualizando planilha")
    sheet.update_cells(cells_to_update, value_input_option=ValueInputOption.user_entered)
    logger.info("Planilha atualizada")
