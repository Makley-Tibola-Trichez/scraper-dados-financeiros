from datetime import datetime
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from src.models.acao import AcaoModel
from src.utils.webdriver import WebDriver

class AcaoService: 
    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver
    
    def scrape(self, ticker: str):
        self._driver.get(f'https://investidor10.com.br/acoes/{ticker}')
        
        cotacao = self._driver.find_element(By.CSS_SELECTOR, "#cards-ticker > div._card.cotacao > div._card-body > div > span").text.strip()
        pl = self._driver.find_element(By.CSS_SELECTOR, '#cards-ticker > div._card.val > div._card-body > span').text.strip()
        pvp = self._driver.find_element(By.CSS_SELECTOR, '#cards-ticker > div._card.vp > div._card-body > span').text.strip()
        dividend_yield = self._driver.find_element(By.CSS_SELECTOR, '#cards-ticker > div._card.dy > div._card-body > span').text.strip()
        payout = self._driver.find_element(By.CSS_SELECTOR, '#table-indicators > div:nth-child(5) > div.value.d-flex.justify-content-between.align-items-center > span').text.strip()
        
        return AcaoModel(
            id=None,
            ticker=ticker, 
            cotacao=cotacao, 
            pl=pl, 
            pvp=pvp, 
            dividend_yield=dividend_yield, 
            payout=payout,
            date=datetime.now().strftime('%Y-%m-%d')
        )
        
        