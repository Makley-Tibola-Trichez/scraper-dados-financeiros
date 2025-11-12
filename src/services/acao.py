from src.models.acao import AcaoModel
from src.utils.webdriver import WebDriver
from src.utils.investidor10 import Investidor10
from src.utils.datetime import DatetimeUtils

class AcaoService: 
    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver
    
    def scrape(self, ticker: str):
        self.__driver.get(f'https://investidor10.com.br/acoes/{ticker}')
        scrap = Investidor10(self.__driver)
        
        cotacao = scrap.get_cotacao()
        pl = scrap.get_pl()
        pvp = scrap.get_pvp()
        dividend_yield = scrap.get_dividend_yield()
        payout = scrap.get_payout()
        setor = scrap.get_setor()
        segmento = scrap.get_segmento_do_setor()
        
        return AcaoModel(
            id=None,
            ticker=ticker, 
            cotacao=cotacao, 
            pl=pl, 
            pvp=pvp, 
            dividend_yield=dividend_yield, 
            payout=payout,
            date=DatetimeUtils.hoje(),
            setor=setor,
            segmento=segmento
        )
        
        