
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from src.constants import TICKERS
from src.models.acao import AcaoModel
from src.services.dividendo import DividendoService
from src.db import inserir_acao_db, obter_acao_db
from src.models.dividendo import DividendoModel
from src.services.acao import AcaoService
from sqlite3 import Connection



def obter_acoes(conn: Connection) -> list[AcaoModel]:
    acoes_com_dados: list[AcaoModel] = []
    acao_service = AcaoService()
    for ticker in TICKERS:
        acao = obter_acao_db(conn, ticker)
        
        if acao is None:
            acao = acao_service.scrape(ticker)
            inserir_acao_db(conn, acao)
            
        acoes_com_dados.append(acao)
        
    acao_service.close()
    return acoes_com_dados
    

def obter_dividendos_anuais() -> list[DividendoModel]:
    dividendo_service = DividendoService()
    dividendos_anuais: list[DividendoModel] = []
    for ticker in TICKERS:
        for dividendo in dividendo_service.scrape(ticker=ticker):
            dividendos_anuais.append(dividendo)
    
    dividendo_service.close()
    return dividendos_anuais
    
    
