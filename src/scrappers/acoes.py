from gspread import Client, Cell
from sqlite3 import Connection
from src.utils.webdriver import WebDriver
from src.utils.datetime import DatetimeUtils
from src.models.acao import AcaoModel
from src.models.dividendo import DividendoModel
from src.repositories.acao import AcaoRepository
from src.repositories.dividendo import DividendoRepository
from src.services.acao import AcaoService
from src.services.dividendo import DividendoService
from gspread.utils import ValueInputOption
from src.utils.formatters import to_brl
from typing import Dict
from src.sheet.acaoCells import AcaoCells
from src.errors import SemHistoricoDeDividendos
 
def scrapperAcoes(
    gc: Client, 
    SAMPLE_SPREADSHEET_ID:str, 
    driver: WebDriver,
    conn: Connection
):
    sheet = gc.open_by_key(SAMPLE_SPREADSHEET_ID).sheet1
    tickers_existentes = sheet.col_values(1)

    acao_service = AcaoService(driver)
    dividendo_service = DividendoService(driver)
    acao_repository = AcaoRepository(conn)
    dividendo_repository = DividendoRepository(conn)
    
    
    acoes: list[AcaoModel] = []
    dividendos_de_acao: Dict[str, list[DividendoModel]] = {}
    HOJE = DatetimeUtils.hoje()
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
        
        dividendos_anuais: list[DividendoModel] | None = dividendo_repository.obter_por_ticker(ticker)
        
        if dividendos_anuais is None:
            dividendos_anuais = []
            try: 
                for dividendo_scrape in dividendo_service.scrape(ticker=str(ticker)):
                    if dividendo_scrape is not None:
                        dividendo_repository.inserir(dividendo_scrape)
                        dividendos_anuais.append(dividendo_scrape)
                        print(f"Dividendo {ticker} inserido no banco de dados.")
                        dividendo_repository.obter_por_ticker(ticker)
                    
                    dividendos_anuais = dividendo_repository.obter_por_ticker(ticker)
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
        
        dividendos_anuais = dividendos_de_acao.get(acao.ticker, [])
        dividendos_values = [to_brl(div.valor) for div in dividendos_anuais]
        dividendos_cells = acaoCells.cells_dividendos(dividendos_values)
        if len(dividendos_cells) > 0: cells_to_update.extend(dividendos_cells)
            
    sheet.update_cells(cells_to_update, value_input_option=ValueInputOption.user_entered)
