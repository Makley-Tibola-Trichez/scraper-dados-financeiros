from collections.abc import Generator

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..errors import SemHistoricoDeDividendosError
from ..models.dividendo import DividendoAnualModel
from ..utils.acessos import acessar_fundamentus
from ..utils.webdriver import WebDriver


class DividendoAnualService:
    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver

    def scrape(self, ticker: str) -> Generator[DividendoAnualModel, None, None]:
        acessar_fundamentus(self._driver, ticker)

        try:
            WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.ID, "chbAgruparAno"))).click()
        except Exception as err:
            raise SemHistoricoDeDividendosError(ticker) from err

        linhas = self._driver.find_elements(By.CSS_SELECTOR, "#resultado-anual > tbody > tr")

        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            ano = colunas[0].text
            valor = float(colunas[1].text.replace("R$", "").replace(",", "."))
            yield DividendoAnualModel(id=None, ticker=ticker, ano=ano, valor=valor, date="")
