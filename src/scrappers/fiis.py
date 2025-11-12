from gspread import Client, Cell
from sqlite3 import Connection
from utils.webdriver import WebDriver
from utils.datetime import DatetimeUtils
from src.models.acao import AcaoModel
from src.models.dividendo import DividendoModel
from src.repositories.acao import AcaoRepository
from src.repositories.dividendo import DividendoRepository
from src.services.acao import AcaoService
from src.services.dividendo import DividendoService
from gspread.utils import ValueInputOption
from src.utils.formatters import to_brl
from typing import Dict

def fiisScrapper(
    gc: Client, 
    SAMPLE_SPREADSHEET_ID:str, 
    driver: WebDriver,
    conn: Connection
):
  sheet = gc.open_by_key(SAMPLE_SPREADSHEET_ID).sheet1
  tickers_existentes = sheet.col_values(1)


  fiis: list[FiiModel] = []
  dividendo_de_fii = Dict[str, list[DividendoModel]] = {}

  HOJE = DatetimeUtils.hoje()


  for ticker in tickers_existentes[2:]:
    ticker = str(ticker)

  pass
