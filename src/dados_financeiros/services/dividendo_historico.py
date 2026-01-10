from datetime import datetime

from selenium.webdriver.common.by import By

from ..models.dividendo import DividendoHistoricoModel
from ..utils.acessos import acessar_acao_investidor10
from ..utils.logger import logger
from ..utils.webdriver import WebDriver


class DividendoHistoricoService:
    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver

    def scrape(self, ticker: str) -> list[DividendoHistoricoModel]:
        acessar_acao_investidor10(self._driver, ticker)

        linhas = self._driver.find_elements(By.CSS_SELECTOR, "#resultado > tbody > tr")

        dividendos_historicos: list[DividendoHistoricoModel] = []
        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            data_anuncio = datetime.strptime(colunas[0].text, "%d/%m/%Y")
            ano_limite = datetime(2020, 1, 1)

            if data_anuncio < ano_limite:
                continue

            data_pagamento = None

            try:
                data_pagamento = datetime.strptime(colunas[3].text, "%d/%m/%Y")
            except Exception as e:
                logger.warning(e)
                pass

            valor = float(colunas[1].text.replace("R$", "").replace(",", "."))
            tipo = colunas[2].text

            dividendos_historicos.append(
                DividendoHistoricoModel(
                    ticker=ticker,
                    valor=valor,
                    data_anuncio=data_anuncio,
                    data_pagamento=data_pagamento,
                    tipo=tipo,
                    data=None,
                )
            )
        return dividendos_historicos
