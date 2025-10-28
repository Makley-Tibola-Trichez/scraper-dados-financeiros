from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.models.dividendo import DividendoModel
from src.utils.webdriver import WebDriver

class DividendoService:
    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver
        
    def scrape(self, ticker: str): 
        self._driver.get(f'https://www.fundamentus.com.br/proventos.php?papel={ticker}&tipo=2')
                
        WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((By.ID, 'chbAgruparAno'))
        ).click()
        
        linhas = self._driver.find_elements(By.CSS_SELECTOR, '#resultado-anual > tbody > tr')
        
        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, 'td')
            ano = colunas[0].text
            valor = float(colunas[1].text.replace('R$', '').replace(',', '.'))
            yield DividendoModel(
                id=None,
                ticker=ticker,
                ano=ano,
                valor=valor,
                date=''
            )