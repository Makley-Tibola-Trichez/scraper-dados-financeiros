from typing import List
from src.utils.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from src.errors import ElementoNaoEncontradoError

class Investidor10:
  __informacoes_sobre_empresa: List[WebElement] | None = None
  __indicadores: List[WebElement] | None = None
  def __init__(self, driver: WebDriver):
    self.__driver = driver

  def get_cotacao(self):
    return self.__driver.find_element(By.CSS_SELECTOR, "#cards-ticker > div._card.cotacao > div._card-body > div > span").text.strip()
  def get_pl(self):
    return self.__driver.find_element(By.CSS_SELECTOR, '#cards-ticker > div._card.val > div._card-body > span').text.strip()
  def get_pvp(self):
    return self.__driver.find_element(By.CSS_SELECTOR, '#cards-ticker > div._card.vp > div._card-body > span').text.strip()
  def get_dividend_yield(self):
    return self.__driver.find_element(By.CSS_SELECTOR, '#cards-ticker > div._card.dy > div._card-body > span').text.strip()
  def get_payout(self):
    indicatores = self.__scrape_indicadores()
    for indicador in indicatores:
      if str(indicador.find_element(By.CSS_SELECTOR, '& > span').text).strip().lower() == 'payout':
        return indicador.find_element(By.CSS_SELECTOR, 'div.value > span').text.strip()

    raise ElementoNaoEncontradoError(seletor='PAYOUT')
  
  def __scrape_indicadores(self): 
    if not self.__indicadores:
      self.__indicadores = self.__driver.find_elements(By.CSS_SELECTOR, '#table-indicators > div')
    return self.__indicadores

    
  def __scrape_informacoes_sobre_empresa(self):
      if not self.__informacoes_sobre_empresa:
        self.__informacoes_sobre_empresa =  self.__driver.find_elements(By.CSS_SELECTOR, '#table-indicators-company > div')
      return self.__informacoes_sobre_empresa

  def get_setor(self):
    informacoes_sobre_empresa = self.__scrape_informacoes_sobre_empresa()
    informacoes_sobre_empresa.reverse()
    
    for elemento in informacoes_sobre_empresa:
      if str(elemento.find_element(By.CSS_SELECTOR, 'span.title').text).strip().lower() == 'setor':
        return elemento.find_element(By.CSS_SELECTOR, 'span.value').text.strip()
    
    raise ElementoNaoEncontradoError(seletor='SETOR')
  
  def get_segmento_do_setor(self):
    informacoes_sobre_empresa = self.__scrape_informacoes_sobre_empresa()
    informacoes_sobre_empresa.reverse()
    
    for elemento in informacoes_sobre_empresa:
      if str(elemento.find_element(By.CSS_SELECTOR, 'span.title').text).strip().lower() == 'segmento':
        return elemento.find_element(By.CSS_SELECTOR, 'span.value').text.strip()
    
    raise ElementoNaoEncontradoError(seletor='SEGMENTO DO SETOR')
  