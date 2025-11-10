from datetime import datetime
import sqlite3

from os import getenv
from googleapiclient.errors import HttpError
import gspread
from gspread.utils import ValueInputOption

from src.models.acao import AcaoModel
from src.models.dividendo import DividendoModel
from src.repositories.acao import AcaoRepository
from src.repositories.dividendo import DividendoRepository
from src.services.acao import AcaoService
from src.services.dividendo import DividendoService
from src.sheet import Cells
from typing import Dict
from dotenv import load_dotenv

from src.utils.webdriver import WebDriver
from src.utils.formatters import to_brl

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = getenv("SPREADSHEET_ID")

print(SAMPLE_SPREADSHEET_ID)


def main():
  if SAMPLE_SPREADSHEET_ID is None:
      raise ValueError("SPREADSHEET_ID environment variable not set")
  try:
    gc = gspread.oauth(credentials_filename='credentials.json', authorized_user_filename='token.json')
    sheet = gc.open_by_key(SAMPLE_SPREADSHEET_ID).sheet1
    
    HOJE = datetime.now().strftime('%Y-%m-%d')
    
    tickers_existentes = sheet.col_values(1)
    conn = sqlite3.connect('acoes.db')
    
    driver = WebDriver()
    acao_service = AcaoService(driver)
    dividendo_service = DividendoService(driver)
    acao_repository = AcaoRepository(conn)
    dividendo_repository = DividendoRepository(conn)
    
    
    acoes: list[AcaoModel] = []
    dividendos_de_acao: Dict[str, list[DividendoModel]] = {}
    
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
        else:
            print(f"Dividendo {ticker} já existe no banco de dados.")
    
    driver.quit()
        
    cells_to_update: list[gspread.Cell] = []
    for acao in acoes:
        if acao.ticker not in tickers_existentes:
            continue
        
        linha = tickers_existentes.index(acao.ticker) + 1
        cell = Cells(linha)
        
        cotacao = cell.cell_cotacao(acao.cotacao)
        if cotacao: cells_to_update.append(cotacao)
        
        pl = cell.cell_pl(acao.pl) 
        if pl: cells_to_update.append(pl)
        
        pvp = cell.cell_pvp(acao.pvp)
        if pvp: cells_to_update.append(pvp)
        
        dividend_yield = cell.cell_dividend_yield(acao.dividend_yield)
        if dividend_yield: cells_to_update.append(dividend_yield)
        
        payout = cell.cell_payout(acao.payout)
        if payout: cells_to_update.append(payout)
        
        dividendos_anuais = dividendos_de_acao.get(acao.ticker, [])
        dividendos_values = [to_brl(div.valor) for div in dividendos_anuais]
        dividendos_cells = cell.cells_dividendos(dividendos_values)
        if len(dividendos_cells) > 0: cells_to_update.extend(dividendos_cells)
        
    sheet.update_cells(cells_to_update, value_input_option=ValueInputOption.user_entered)
    
    conn.close()
  except HttpError as err:
    print(err)
  

