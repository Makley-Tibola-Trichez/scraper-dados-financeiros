from datetime import timedelta
from sqlite3 import Connection
from typing import cast

from gspread import Cell, Client
from gspread.utils import ValueInputOption
from playwright.sync_api import Page

from ..acao.application.salvar_dados_acoes_use_case import SalvarAcaoUseCase
from ..acao.infrastructure.acao_investidor10_gateway import AcaoInvestidor10Gateway
from ..acao.infrastructure.acao_repository import AcaoRepository
from ..config.config import Config
from ..sheet.acao_cols import AcaoCols
from ..sheet.cell_builder import build_cells
from ..utils.datetime import DatetimeUtils
from ..utils.formatters import to_br_decimal, to_brl
from ..utils.logger import logger
from ..utils.progresso_processo import ProgressoProcessos


def scrapper_acoes(
    gc: Client,
    spreadsheet_id: str,
    page: Page,
    conn: Connection,
) -> None:
    sheet = gc.open_by_key(spreadsheet_id).get_worksheet_by_id(Config.id_worksheet_acoes_teto_bazin)
    tickers_existentes = cast(list[str], sheet.col_values(1))
    # tickers_existentes = list(set(tickers_existentes).difference(set(LISTA_DE_TICKERS_EXCLUSAO)))
    # tickers_existentes.sort()

    acao_repository = AcaoRepository(conn, logger)
    pagina_acao_gateway = AcaoInvestidor10Gateway(page, logger)
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

        valores: list[tuple[AcaoCols, str | None]] = [
            (AcaoCols.COTACAO, to_br_decimal(acao.cotacao)),
            (AcaoCols.PL, acao.pl),
            (AcaoCols.PVP, acao.pvp),
            (AcaoCols.VPA, acao.vpa),
            (AcaoCols.LPA, acao.lpa),
            (AcaoCols.ROE, acao.roe),
            (AcaoCols.DIVIDEND_YIELD, acao.dy),
            (AcaoCols.PAYOUT, acao.payout),
            (AcaoCols.SETOR, acao.setor),
            (AcaoCols.SEGMENTO, acao.segmento),
            (AcaoCols.MEDIA_DIVIDENDOS_12_MESES, to_br_decimal(dividendo_medio_12_meses)),
            (AcaoCols.DIVIDENDO_ANUAL_2026, to_brl(soma_dividendos_por_ano["2026"] or 0)),
            (AcaoCols.DIVIDENDO_ANUAL_2025, to_brl(soma_dividendos_por_ano["2025"] or 0)),
            (AcaoCols.DIVIDENDO_ANUAL_2024, to_brl(soma_dividendos_por_ano["2024"] or 0)),
            (AcaoCols.DIVIDENDO_ANUAL_2023, to_brl(soma_dividendos_por_ano["2023"] or 0)),
            (AcaoCols.DIVIDENDO_ANUAL_2022, to_brl(soma_dividendos_por_ano["2022"] or 0)),
        ]

        cells_to_update.extend(build_cells(linha, valores))

    if not cells_to_update:
        logger.warning("Nenhuma célula para atualizar (nenhuma ação processada com sucesso)")
        return

    logger.info("Atualizando planilha")
    sheet.update_cells(cells_to_update, value_input_option=ValueInputOption.user_entered)
    logger.info("Planilha atualizada")
