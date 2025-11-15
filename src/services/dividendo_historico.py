from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime 

from src.models.dividendo import DividendoAnualModel, DividendoHistoricoModel
from src.utils.webdriver import WebDriver
from src.errors import SemHistoricoDeDividendos

class DividendoHistoricoService:
    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver
        
    def scrape(self, ticker: str): 
        self._driver.get(f'https://www.fundamentus.com.br/proventos.php?papel={ticker}&tipo=2')
        
        # try:
        #     WebDriverWait(self._driver, 10).until(
        #         EC.presence_of_element_located((By.ID, 'chbAgruparAno'))
        #     ).click()
        # except:
        #     raise SemHistoricoDeDividendos(ticker)
      
        
        linhas = self._driver.find_elements(By.CSS_SELECTOR, '#resultado > tbody > tr')
        
        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, 'td')
            data_anuncio = datetime.strptime(colunas[0].text, "%d/%m/%Y")
            ano_limite = datetime(2020,1,1)
            
            if data_anuncio < ano_limite:
                continue
            
            data_pagamento = None
            
            try:
                data_pagamento = datetime.strptime(colunas[3].text, "%d/%m/%Y")
            except:
                pass
            
            valor = float(colunas[1].text.replace('R$', '').replace(',', '.'))
            tipo = colunas[2].text
            
            yield DividendoHistoricoModel(
                ticker=ticker,
                valor=valor,
                data_anuncio=data_anuncio,
                data_pagamento=data_pagamento,
                tipo=tipo,
                data=None
            )