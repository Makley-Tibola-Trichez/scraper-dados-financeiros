from datetime import timedelta
from sqlite3 import Connection
from typing import cast

from gspread import Cell, Client
from gspread.utils import ValueInputOption

from ..acao.application.salvar_dados_acoes_use_case import SalvarAcaoUseCase
from ..acao.infrastructure.acao_investidor10_gateway import AcaoInvestidor10Gateway
from ..acao.infrastructure.acao_repository import AcaoRepository
from ..config.config import Config
from ..sheet.acao_cells import AcaoCells
from ..utils.datetime import DatetimeUtils
from ..utils.formatters import to_brl
from ..utils.logger import logger
from ..utils.progresso_processo import ProgressoProcessos
from ..utils.webdriver import WebDriver


def scrapper_acoes(
    gc: Client,
    spreadsheet_id: str,
    driver: WebDriver,
    conn: Connection,
) -> None:
    sheet = gc.open_by_key(spreadsheet_id).get_worksheet_by_id(Config.id_worksheet_acoes_teto_bazin)
    tickers_existentes = cast(list[str], sheet.col_values(1))

    acao_repository = AcaoRepository(conn, logger)
    pagina_acao_gateway = AcaoInvestidor10Gateway(driver, logger)

    salvar_acao_use_case = SalvarAcaoUseCase(logger, pagina_acao_gateway, acao_repository)

    acoes = salvar_acao_use_case.executar(tickers_existentes[2:])

    cells_to_update: list[Cell] = []

    processo_atualizacao_planilhas_acoes = ProgressoProcessos(
        total_processos=len(acoes),
        descricao_tipo_processo="Atualização de Planilha de Ações",
    )

    for acao in acoes:
        processo_atualizacao_planilhas_acoes.atualizar_progresso(
            nome_processo=acao.ticker, indice_processo=acoes.index(acao) + 1
        )
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

        dividend_yield = acao_cells.cell_dividend_yield(acao.dy)
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
        agora = DatetimeUtils.hoje_datetime()
        um_ano_atras = agora - timedelta(days=365)
        # Faz o cálculo de média de dividendos do último 1 ano
        dividendos_12_meses = list(
            filter(
                lambda d: um_ano_atras <= d.data_anuncio <= agora,
                acao.dividendos,
            )
        )
        soma_dividendos_12_meses = 0
        for div in dividendos_12_meses:
            soma_dividendos_12_meses += div.valor

        dividendo_medio_12_meses = soma_dividendos_12_meses / (len(dividendos_12_meses) or 1)
        dividendo_medio_12_meses_cell = acao_cells.cell_media_dividendos_12_meses(to_brl(dividendo_medio_12_meses))
        if dividendo_medio_12_meses_cell:
            cells_to_update.append(dividendo_medio_12_meses_cell)

        # Agrupa total de dividendos por ano
        soma_dividendos_por_ano: dict[str, float] = {
            "2026": 0,
            "2025": 0,
            "2024": 0,
            "2023": 0,
            "2022": 0,
        }

        for div in acao.dividendos:
            key = str(div.data_anuncio.year)

            if key not in soma_dividendos_por_ano:
                soma_dividendos_por_ano[key] = 0

            soma_dividendos_por_ano[key] += div.valor

        # for k, v in soma_dividendos_por_ano.items():
        #     print(f"{acao.ticker} | {k} = {v} {to_brl(v)}")
        #     print()
        # input()

        cell_2026 = acao_cells.dividendo_ano_2026(to_brl(soma_dividendos_por_ano["2026"] or 0))
        if cell_2026:
            cells_to_update.append(cell_2026)
        cell_2025 = acao_cells.dividendo_ano_2025(to_brl(soma_dividendos_por_ano["2025"] or 0))
        if cell_2025:
            cells_to_update.append(cell_2025)
        cell_2024 = acao_cells.dividendo_ano_2024(to_brl(soma_dividendos_por_ano["2024"] or 0))
        if cell_2024:
            cells_to_update.append(cell_2024)
        cell_2023 = acao_cells.dividendo_ano_2023(to_brl(soma_dividendos_por_ano["2023"] or 0))
        if cell_2023:
            cells_to_update.append(cell_2023)
        cell_2022 = acao_cells.dividendo_ano_2022(to_brl(soma_dividendos_por_ano["2022"] or 0))
        if cell_2022:
            cells_to_update.append(cell_2022)

        # dividendos_values = [to_brl(float(div.valor)) for div in acao.dividendos]
        # dividendos_cells = acao_cells.cells_dividendos(dividendos_values)
        # if len(dividendos_cells) > 0:
        #     cells_to_update.extend(dividendos_cells)

    logger.info("Atualizando planilha")
    sheet.update_cells(cells_to_update, value_input_option=ValueInputOption.user_entered)
    logger.info("Planilha atualizada")
