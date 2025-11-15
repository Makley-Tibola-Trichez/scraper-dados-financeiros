from gspread import Client, Cell
from sqlite3 import Connection
from src.services.dividendo_historico import DividendoHistoricoService
from src.utils.webdriver import WebDriver
from src.utils.datetime import DatetimeUtils
from src.models.acao import AcaoModel
from src.models.dividendo import DividendoAnualModel, DividendoHistoricoModel
from src.repositories.acao import AcaoRepository
from src.repositories.dividendo_historico import DividendoHistoricoRepository
from src.repositories.dividendo_anual import DividendoAnualRepository
from src.services.acao import AcaoService
from src.services.dividendo_anual import DividendoAnualService
from gspread.utils import ValueInputOption
from src.utils.formatters import to_brl
from typing import Dict
from src.sheet.acaoCells import AcaoCells
from src.errors import SemHistoricoDeDividendos
from datetime import datetime, timedelta
 
def scrapperAcoes(
    gc: Client, 
    SAMPLE_SPREADSHEET_ID:str, 
    driver: WebDriver,
    conn: Connection
):
    sheet = gc.open_by_key(SAMPLE_SPREADSHEET_ID).sheet1
    tickers_existentes = sheet.col_values(1)

    acao_service = AcaoService(driver)
    dividendo_anual_service = DividendoAnualService(driver)
    dividendo_historico_service = DividendoHistoricoService(driver)
    acao_repository = AcaoRepository(conn)
    dividendo_anual_repository = DividendoAnualRepository(conn)
    dividendo_historico_repository = DividendoHistoricoRepository(conn)
    
    
    acoes: list[AcaoModel] = []
    dividendos_de_acao: Dict[str, list[DividendoAnualModel]] = {}
    medias_dividendos_meses: Dict[str, float] = {}
    HOJE = DatetimeUtils.hoje()
    um_ano_atras = DatetimeUtils.hoje_datetime() - timedelta(days=365)
    for ticker in tickers_existentes[2:]:
        ticker = str(ticker)
        
        acao = acao_repository.obter_por_ticker_e_data(ticker, HOJE)
        if acao is None:
            acao = acao_service.scrape(ticker=str(ticker))
            if acao is not None:
                acao_repository.inserir(acao)
                print(f"Ação {ticker} inserida no banco de dados.")
            else:
                print(f"Ação {ticker} não encontrada.")
        else:
            print(f"Ação {ticker} já existe no banco de dados para a data {HOJE}.")
        
        if acao is not None:
            acoes.append(acao)
        
        dividendos_anuais: list[DividendoAnualModel] | None = dividendo_anual_repository.obter_por_ticker(ticker)

        quantidade_dividendos_ultimos_12_meses = 0
        total_dividendos_ultimos_12_meses = 0
        for dividendo_scrape in dividendo_historico_service.scrape(ticker=str(ticker)):
            if dividendo_scrape is not None:
                dividendo_historico = (dividendo_historico_repository.inserir(dividendo_scrape))
                if um_ano_atras <= dividendo_historico.data_anuncio <= DatetimeUtils.hoje_datetime():
                    quantidade_dividendos_ultimos_12_meses += 1
                    total_dividendos_ultimos_12_meses += dividendo_historico.valor
        
        media_dividendos_ultimos_12_meses = round(total_dividendos_ultimos_12_meses / quantidade_dividendos_ultimos_12_meses, 2) if quantidade_dividendos_ultimos_12_meses > 0 else 0
        medias_dividendos_meses[str(ticker)] = media_dividendos_ultimos_12_meses
        
                
        
        if dividendos_anuais is None:
            dividendos_anuais = []
            try: 
                for dividendo_scrape in dividendo_anual_service.scrape(ticker=str(ticker)):
                    if dividendo_scrape is not None:
                        dividendo_anual_repository.inserir(dividendo_scrape)
                        dividendos_anuais.append(dividendo_scrape)
                        print(f"Dividendo {ticker} inserido no banco de dados.")
                    
                    dividendos_anuais = dividendo_anual_repository.obter_por_ticker(ticker)
                    if dividendos_anuais is None or len(dividendos_anuais) == 0:
                        print(f"Dividendo {ticker} não encontrado.")
                    else:
                        dividendos_de_acao[ticker] = dividendos_anuais
            except SemHistoricoDeDividendos as e:
                print(e.mensagem)
                continue
        else:
            dividendos_de_acao[ticker] = dividendos_anuais
            print(f"[{ticker}] - Dividendo já existe no banco de dados.")
    
    driver.quit()
        
    cells_to_update: list[Cell] = []
    for acao in acoes:
        if acao.ticker not in tickers_existentes:
            continue
        
        linha = tickers_existentes.index(acao.ticker) + 1
        acaoCells = AcaoCells(linha)
        
        cotacao = acaoCells.cell_cotacao(acao.cotacao)
        if cotacao: cells_to_update.append(cotacao)
        
        pl = acaoCells.cell_pl(acao.pl) 
        if pl: cells_to_update.append(pl)
        
        pvp = acaoCells.cell_pvp(acao.pvp)
        if pvp: cells_to_update.append(pvp)
        
        dividend_yield = acaoCells.cell_dividend_yield(acao.dividend_yield)
        if dividend_yield: cells_to_update.append(dividend_yield)
        
        payout = acaoCells.cell_payout(acao.payout)
        if payout: cells_to_update.append(payout)
        
        setor = acaoCells.cell_setor(acao.setor)
        if setor: cells_to_update.append(setor)
        
        segmento = acaoCells.cell_segmento_do_certo(acao.segmento)
        if segmento: cells_to_update.append(segmento)
        
        dividendo_medio_12_meses = medias_dividendos_meses.get(acao.ticker, 0)
        dividendo_medio_12_meses_value = to_brl(dividendo_medio_12_meses)
        
        dividendo_medio_12_meses_cell = acaoCells.cell_media_dividendos_12_meses(dividendo_medio_12_meses_value)
        if dividendo_medio_12_meses_cell: cells_to_update.append(dividendo_medio_12_meses_cell)
        
        dividendos_anuais = dividendos_de_acao.get(acao.ticker, [])
        dividendos_values = [to_brl(div.valor) for div in dividendos_anuais]
        dividendos_cells = acaoCells.cells_dividendos(dividendos_values)
        if len(dividendos_cells) > 0: cells_to_update.extend(dividendos_cells)
            
    sheet.update_cells(cells_to_update, value_input_option=ValueInputOption.user_entered)
