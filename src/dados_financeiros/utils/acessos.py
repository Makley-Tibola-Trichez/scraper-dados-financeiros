from .webdriver import WebDriver


def acessar_fundamentus_proventos(driver: WebDriver, ticker: str) -> None:
    driver.get(f"https://www.fundamentus.com.br/proventos.php?papel={ticker}&tipo=2")


def acessar_acao_investidor10(driver: WebDriver, ticker: str) -> None:
    driver.get(f"https://investidor10.com.br/acoes/{ticker}")


def acessar_fii_investidor10(driver: WebDriver, ticker: str) -> None:
    driver.get(f"https://investidor10.com.br/fiis/{ticker}")
