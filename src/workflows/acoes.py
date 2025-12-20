from datetime import timedelta
from sqlite3 import Connection

from gspread import Cell, Client
from gspread.utils import ValueInputOption

from ..config.config import Config
from ..errors import SemHistoricoDeDividendosError
from ..models.acao import AcaoModel
from ..models.dividendo import DividendoAnualModel
from ..repositories.acao import AcaoRepository
from ..repositories.dividendo_anual import DividendoAnualRepository
from ..repositories.dividendo_historico import DividendoHistoricoRepository
from ..services.acao import AcaoService
from ..services.dividendo_anual import DividendoAnualService
from ..services.dividendo_historico import DividendoHistoricoService
from ..sheet.acao_cells import AcaoCells
from ..utils.datetime import DatetimeUtils
from ..utils.formatters import to_brl
from ..utils.logger import logger
from ..utils.webdriver import WebDriver


def scrapper_acoes(
    gc: Client,
    spreadsheet_id: str,
    driver: WebDriver,
    conn: Connection,
) -> None:
    sheet = gc.open_by_key(spreadsheet_id).get_worksheet_by_id(Config.id_worksheet_acoes_teto_bazin)
    tickers_existentes = sheet.col_values(1)

    acao_service = AcaoService(driver, logger)
    dividendo_anual_service = DividendoAnualService(driver)
    dividendo_historico_service = DividendoHistoricoService(driver)
    acao_repository = AcaoRepository(conn)
    dividendo_anual_repository = DividendoAnualRepository(conn)
    dividendo_historico_repository = DividendoHistoricoRepository(conn)

    tickers = acao_repository.verificar_se_existem_tickers(tickers_existentes[2:], DatetimeUtils.hoje())

    acoes: list[AcaoModel] = []
    dividendos_de_acao: dict[str, list[DividendoAnualModel]] = {}
    medias_dividendos_meses: dict[str, float] = {}
    hoje = DatetimeUtils.hoje()
    um_ano_atras = DatetimeUtils.hoje_datetime() - timedelta(days=365)

    for ticker, acao in tickers:
        if acao is not None:
            logger.info(f"Ação {ticker} já existe no banco de dados para a data {hoje}.")
            acoes.append(acao)
        else:
            acao = acao_service.scrape(ticker=str(ticker))
            if acao is not None:
                acao = acao_repository.inserir(acao)
                acoes.append(acao)
                logger.info(f"Ação {ticker} inserida no banco de dados.")
            else:
                logger.warning(f"Ação {ticker} não encontrada.")

        dividendos_anuais: list[DividendoAnualModel] | None = dividendo_anual_repository.obter_por_ticker(ticker)

        quantidade_dividendos_ultimos_12_meses = 0
        total_dividendos_ultimos_12_meses = 0

        dividendos_historicos = dividendo_historico_service.scrape(ticker=str(ticker))
        dividendos_historicos = dividendo_historico_repository.inserir(dividendos_historicos)
        for dividendo_historico in dividendos_historicos:
            if um_ano_atras <= dividendo_historico.data_anuncio <= DatetimeUtils.hoje_datetime():
                quantidade_dividendos_ultimos_12_meses += 1
                total_dividendos_ultimos_12_meses += dividendo_historico.valor

        media_dividendos_ultimos_12_meses = (
            round(
                total_dividendos_ultimos_12_meses / quantidade_dividendos_ultimos_12_meses,
                2,
            )
            if quantidade_dividendos_ultimos_12_meses > 0
            else 0
        )
        medias_dividendos_meses[str(ticker)] = media_dividendos_ultimos_12_meses

        if dividendos_anuais is None:
            dividendos_anuais = []
            try:
                for dividendo_scrape in dividendo_anual_service.scrape(ticker=str(ticker)):
                    if dividendo_scrape is not None:
                        dividendo_anual_repository.inserir(dividendo_scrape)
                        dividendos_anuais.append(dividendo_scrape)
                        logger.info(f"Dividendo {ticker} inserido no banco de dados.")

                    dividendos_anuais = dividendo_anual_repository.obter_por_ticker(ticker)
                    if dividendos_anuais is None or len(dividendos_anuais) == 0:
                        logger.info(f"Dividendo {ticker} não encontrado.")
                    else:
                        dividendos_de_acao[ticker] = dividendos_anuais
            except SemHistoricoDeDividendosError as e:
                logger.warning(e.mensagem)
                continue
        else:
            dividendos_de_acao[ticker] = dividendos_anuais
            logger.info(f"[{ticker}] - Dividendo já existe no banco de dados.")

    cells_to_update: list[Cell] = []
    for acao in acoes:
        if acao.ticker not in tickers_existentes:
            continue

        logger.info(f"{acao.ticker}, gerando células com novos valores")
        linha = tickers_existentes.index(acao.ticker) + 1
        acao_cells = AcaoCells(linha)

        cotacao = acao_cells.cell_cotacao(acao.cotacao)
        if cotacao:
            cells_to_update.append(cotacao)

        pl = acao_cells.cell_pl(acao.pl)
        if pl:
            cells_to_update.append(pl)

        pvp = acao_cells.cell_pvp(acao.pvp)
        if pvp:
            cells_to_update.append(pvp)

        vpa = acao_cells.cell_vpa(acao.vpa)
        if vpa:
            cells_to_update.append(vpa)

        lpa = acao_cells.cell_lpa(acao.lpa)
        if lpa:
            cells_to_update.append(lpa)

        roe = acao_cells.cell_roe(acao.roe)
        if roe:
            cells_to_update.append(roe)

        dividend_yield = acao_cells.cell_dividend_yield(acao.dividend_yield)
        if dividend_yield:
            cells_to_update.append(dividend_yield)

        payout = acao_cells.cell_payout(acao.payout)
        if payout:
            cells_to_update.append(payout)

        setor = acao_cells.cell_setor(acao.setor)
        if setor:
            cells_to_update.append(setor)

        segmento = acao_cells.cell_segmento_do_certo(acao.segmento)
        if segmento:
            cells_to_update.append(segmento)

        dividendo_medio_12_meses = medias_dividendos_meses.get(acao.ticker, 0)
        dividendo_medio_12_meses_value = to_brl(dividendo_medio_12_meses)

        dividendo_medio_12_meses_cell = acao_cells.cell_media_dividendos_12_meses(dividendo_medio_12_meses_value)
        if dividendo_medio_12_meses_cell:
            cells_to_update.append(dividendo_medio_12_meses_cell)

        dividendos_anuais = dividendos_de_acao.get(acao.ticker, [])
        dividendos_values = [to_brl(div.valor) for div in dividendos_anuais]
        dividendos_cells = acao_cells.cells_dividendos(dividendos_values)
        if len(dividendos_cells) > 0:
            cells_to_update.extend(dividendos_cells)

    logger.info("Atualizando planilha")
    sheet.update_cells(cells_to_update, value_input_option=ValueInputOption.user_entered)
    logger.info("Planilha atualizada")
