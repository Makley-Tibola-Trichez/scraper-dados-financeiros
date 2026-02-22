from datetime import datetime
from enum import StrEnum
from logging import Logger

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from dados_financeiros.acao.domain.interfaces import IAcaoInvestidor10Gateway
from dados_financeiros.acao.domain.value_objects import Acao, Dividendo
from dados_financeiros.errors import ElementoNaoEncontradoError
from dados_financeiros.utils.webdriver import WebDriver


class TipoIndicador(StrEnum):
    VPA = "vpa"
    ROA = "roa"
    LPA = "lpa"
    ROE = "roe"
    ROIC = "roic"
    PAYOUT = "payout"
    CAGR_RECEITAS_5_ANOS = "cagr receitas 5 anos"
    CAGR_LUCROS_5_ANOS = "cagr lucros 5 anos"
    DIVIDA_LIQUIDA_PATRIMONIO = "dívida líquida / patrimônio"
    DIVIDA_LIQUIDA_EBIT = "dívida líquida / ebit"
    DIVIDA_LIQUIDA_EBITDA = "dívida líquida / ebitda"
    DIVIDA_BRUTA_PATRIMONIO = "dívida bruta / patrimônio"


class AcaoInvestidor10Gateway(IAcaoInvestidor10Gateway):
    def __init__(self, driver: WebDriver, logger: Logger) -> None:
        self._driver = driver
        self._logger = logger
        # self._indicadores: list[WebElement] | None = None
        # self._informacoes_sobre_empresa: list[WebElement] | None = None

    def _acessar(self, ticker: str) -> None:
        url = f"https://investidor10.com.br/acoes/{ticker}"
        self._logger.info(f"Acessando página ({url})")
        self._driver.get(url)

    def _acessar_fundamentus_proventos(self, ticker: str) -> None:
        url = f"https://www.fundamentus.com.br/proventos.php?papel={ticker}&tipo=2"
        self._logger.info(f"Acessando página ({url})")
        self._driver.get(url)

    def fechar(self) -> None:
        self._driver.close()

    def obter_dados(self, ticker: str) -> Acao:
        self._acessar(ticker)

        cotacao = self.obter_cotacao()
        pl = self.obter_pl()
        pvp = self.obter_pvp()
        vpa = self.obter_vpa()
        lpa = self.obter_lpa()
        roe = self.obter_roe()
        dy = self.obter_dy()
        payout = self.obter_payout()
        setor = self.obter_setor()
        segmento = self.obter_segmento_do_setor()
        roic = self.obter_roic()
        roa = self.obter_roa()
        cagr_l = self.cagr_lucros_5_anos()
        cagr_r = self.cagr_receitas_5_anos()

        db_patrimonio = self.db_patrimonio()
        dl_ebit = self.dl_ebit()
        dl_ebitda = self.dl_ebitda()
        dl_patrimonio = self.dl_patrimonio()

        dividendos = self.obter_dividendos(ticker)

        return Acao(
            ticker=ticker,
            cotacao=cotacao,
            pl=pl,
            pvp=pvp,
            vpa=vpa,
            lpa=lpa,
            roe=roe,
            dy=dy,
            payout=payout,
            setor=setor,
            segmento=segmento,
            cagr_lucros_5_anos=cagr_l,
            cagr_receitas_5_anos=cagr_r,
            db_patrimonio=db_patrimonio,
            dl_ebit=dl_ebit,
            dl_ebitda=dl_ebitda,
            dl_patrimonio=dl_patrimonio,
            roa=roa,
            roic=roic,
            dividendos=dividendos,
        )

    def obter_cotacao(self) -> str:
        return self._driver.find_element(
            By.CSS_SELECTOR,
            "#cards-ticker > div._card.cotacao > div._card-body > div > span",
        ).text.strip()

    def obter_pl(self) -> str:
        return self._driver.find_element(
            By.CSS_SELECTOR, "#cards-ticker > div._card.val > div._card-body > span"
        ).text.strip()

    def obter_pvp(self) -> str:
        return self._driver.find_element(
            By.CSS_SELECTOR, "#cards-ticker > div._card.vp > div._card-body > span"
        ).text.strip()

    def obter_vpa(self) -> str:
        indicador = self._obter_indicador(TipoIndicador.VPA)

        if not indicador:
            raise ElementoNaoEncontradoError(seletor="VPA")
        return indicador

    def obter_roa(self) -> str:
        indicador = self._obter_indicador(TipoIndicador.ROA)

        if not indicador:
            raise ElementoNaoEncontradoError(seletor="ROA")
        return indicador

    def obter_lpa(self) -> str:
        indicador = self._obter_indicador(TipoIndicador.LPA)

        if not indicador:
            raise ElementoNaoEncontradoError(seletor="LPA")
        return indicador

    def obter_roe(self) -> str:
        indicador = self._obter_indicador(TipoIndicador.ROE)

        if not indicador:
            raise ElementoNaoEncontradoError(seletor="ROE")
        return indicador

    def obter_roic(self) -> str:
        indicador = self._obter_indicador(TipoIndicador.ROIC)

        if not indicador:
            raise ElementoNaoEncontradoError(seletor="ROIC")
        return indicador

    def obter_dy(self) -> str:
        return self._driver.find_element(
            By.CSS_SELECTOR, "#cards-ticker > div._card.dy > div._card-body > span"
        ).text.strip()

    def obter_payout(self) -> str:
        indicador = self._obter_indicador(TipoIndicador.PAYOUT)

        if not indicador:
            raise ElementoNaoEncontradoError(seletor="PAYOUT")
        return indicador

    def cagr_lucros_5_anos(self) -> str:
        indicador = self._obter_indicador(TipoIndicador.CAGR_RECEITAS_5_ANOS)

        if not indicador:
            erro = ElementoNaoEncontradoError(seletor="CAGR RECEITAS 5 ANOS ")
            self._logger.warning(erro)
            return ""

        return indicador

    def cagr_receitas_5_anos(self) -> str:
        indicador = self._obter_indicador(TipoIndicador.CAGR_LUCROS_5_ANOS)

        if not indicador:
            erro = ElementoNaoEncontradoError(seletor="CAGR LUCROS 5 ANOS ")
            self._logger.warning(erro)
            return ""

        return indicador

    def db_patrimonio(self) -> str:
        indicador = self._obter_indicador(TipoIndicador.DIVIDA_LIQUIDA_PATRIMONIO)

        if not indicador:
            erro = ElementoNaoEncontradoError(seletor="DÍVIDA LÍQUIDA / PATRIMÔNIO")
            self._logger.warning(erro)
            return ""
        return indicador

    def dl_ebit(self) -> str:
        indicador = self._obter_indicador(TipoIndicador.DIVIDA_LIQUIDA_EBIT)

        if not indicador:
            erro = ElementoNaoEncontradoError(seletor="DÍVIDA LÍQUIDA / EBIT")
            self._logger.warning(erro)
            return ""

        return indicador

    def dl_ebitda(self) -> str:
        indicador = self._obter_indicador(TipoIndicador.DIVIDA_LIQUIDA_EBITDA)

        if not indicador:
            erro = ElementoNaoEncontradoError(seletor="DÍVIDA LÍQUIDA / EBITDA")
            self._logger.warning(erro)
            return ""

        return indicador

    def dl_patrimonio(self) -> str:
        indicador = self._obter_indicador(TipoIndicador.DIVIDA_BRUTA_PATRIMONIO)

        if not indicador:
            erro = ElementoNaoEncontradoError(seletor="DÍVIDA BRUTA / PATRIMÔNIO")
            self._logger.warning(erro)
            return ""
        return indicador

    def _obter_indicador(self, tipo_indicador: StrEnum) -> str | None:
        try:
            indicadores = self.__scrape_indicadores()
            for indicador in indicadores:
                if (
                    str(indicador.find_element(By.CSS_SELECTOR, "& > span").text).strip().lower()
                    == tipo_indicador.value
                ):
                    return indicador.find_element(By.CSS_SELECTOR, "div.value > span").text.strip()

            return None
        except Exception as _:
            self._logger.warning(f"Ocorreu algum problema ao buscar o '{tipo_indicador.name}'")
            return None

    def __scrape_indicadores(self) -> list[WebElement]:
        return WebDriverWait(self._driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#table-indicators > div"))
        )

    def __scrape_informacoes_sobre_empresa(self) -> list[WebElement]:
        return WebDriverWait(self._driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#table-indicators-company > div"))
        )

    def obter_setor(self) -> str:
        informacoes_sobre_empresa = self.__scrape_informacoes_sobre_empresa()
        informacoes_sobre_empresa.reverse()

        for elemento in informacoes_sobre_empresa:
            if str(elemento.find_element(By.CSS_SELECTOR, "span.title").text).strip().lower() == "setor":
                return elemento.find_element(By.CSS_SELECTOR, "span.value").text.strip()

        raise ElementoNaoEncontradoError(seletor="SETOR")

    def obter_segmento_do_setor(self) -> str:
        informacoes_sobre_empresa = self.__scrape_informacoes_sobre_empresa()
        informacoes_sobre_empresa.reverse()

        for elemento in informacoes_sobre_empresa:
            if str(elemento.find_element(By.CSS_SELECTOR, "span.title").text).strip().lower() == "segmento":
                return elemento.find_element(By.CSS_SELECTOR, "span.value").text.strip()

        raise ElementoNaoEncontradoError(seletor="SEGMENTO DO SETOR")

    def obter_dividendos(self, ticker: str) -> list[Dividendo]:
        self._acessar_fundamentus_proventos(ticker)

        linhas = self._driver.find_elements(By.CSS_SELECTOR, "#resultado > tbody > tr")

        dividendos_historicos: list[Dividendo] = []
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
                self._logger.warning(e)

            valor = float(colunas[1].text.replace("R$", "").replace(",", "."))
            tipo = colunas[2].text

            dividendos_historicos.append(
                Dividendo(
                    valor=valor,
                    data_anuncio=data_anuncio,
                    data_pagamento=str(data_pagamento),
                    tipo=tipo,
                )
            )
        return dividendos_historicos
