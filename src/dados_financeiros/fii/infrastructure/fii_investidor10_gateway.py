from logging import Logger

from playwright.sync_api import Locator, Page

from dados_financeiros.errors import ElementoNaoEncontradoError
from dados_financeiros.fii.domain.value_objects import Fii
from dados_financeiros.utils.formatters import from_brl

from ..domain.interfaces import IFiiInvestidor10Gateway


class FiiInvestidor10Gateway(IFiiInvestidor10Gateway):
    def __init__(self, page: Page, logger: Logger) -> None:
        self._page = page
        self._logger = logger

    def _acessar(self, ticker: str) -> None:
        self._logger.info(f"Acessando página (https://investidor10.com.br/fiis/{ticker})")
        self._page.goto(f"https://investidor10.com.br/fiis/{ticker}")

    def fechar(self) -> None:
        self._page.close()

    def obter_dados(self, ticker: str) -> Fii:
        self._acessar(ticker)

        cotacao = self.obter_cotacao()
        pvp = self.obter_pvp()
        segmento = self.obter_segmento()
        tipo_de_fundo = self.obter_tipo_de_fundo()
        quantidade_cotas_emitidas = self.obter_quantidade_cotas_emitidas()
        valor_patrimonial_por_cota = self.obter_valor_patrimonial_por_cota()

        dividend_yield_1_mes, dividendo_1_mes = self.obter_dividend_yield_1_mes()
        dividend_yield_3_meses, dividendo_3_meses = self.obter_dividend_yield_3_meses()
        dividend_yield_6_meses, dividendo_6_meses = self.obter_dividend_yield_6_meses()
        dividend_yield_12_meses, dividendo_12_meses = self.obter_dividend_yield_12_meses()

        return Fii(
            cotacao=float(cotacao),
            ticker=ticker,
            pvp=pvp,
            segmento=segmento,
            tipo_de_fundo=tipo_de_fundo,
            quantidade_cotas_emitidas=quantidade_cotas_emitidas,
            valor_patrimonial_por_cota=valor_patrimonial_por_cota,
            dividendo_1_mes=dividendo_1_mes,
            dividendo_3_meses=dividendo_3_meses,
            dividendo_6_meses=dividendo_6_meses,
            dividendo_12_meses=dividendo_12_meses,
            dividend_yield_1_mes=dividend_yield_1_mes,
            dividend_yield_3_meses=dividend_yield_3_meses,
            dividend_yield_6_meses=dividend_yield_6_meses,
            dividend_yield_12_meses=dividend_yield_12_meses,
        )

    def obter_cotacao(self) -> str:
        seletor = "#cards-ticker > div._card.cotacao > div._card-body > div > span.value"
        conteudo = self._page.locator(seletor).text_content()
        if not conteudo:
            raise ElementoNaoEncontradoError(seletor=seletor)
        conteudo = conteudo.strip()
        return from_brl(conteudo)

    def obter_dividend_yield_1_mes(self) -> tuple[str, str]:
        seletor_dy = "#yield-distribuition > div > div.content--info > div:nth-child(1) > span.content--info--item--value:not(.amount)"
        conteudo_dy = self._page.locator(seletor_dy).text_content()

        if not conteudo_dy:
            raise ElementoNaoEncontradoError(seletor=seletor_dy)
        dividend_yield = conteudo_dy.strip()

        seletor_d_pago = (
            "#yield-distribuition > div > div.content--info > div:nth-child(1) > span.content--info--item--value.amount"
        )
        conteudo_d_pago = self._page.locator(seletor_d_pago).text_content()

        if not conteudo_d_pago:
            raise ElementoNaoEncontradoError()

        dividendo_pago = conteudo_d_pago.strip()

        return (dividend_yield, dividendo_pago)

    def obter_dividend_yield_3_meses(self) -> tuple[str, str]:
        seletor_dy = "#yield-distribuition > div > div.content--info > div:nth-child(2) > span.content--info--item--value:not(.amount)"
        conteudo_dy = self._page.locator(seletor_dy).text_content()

        if not conteudo_dy:
            raise ElementoNaoEncontradoError(seletor=seletor_dy)
        dividend_yield = conteudo_dy.strip()

        seletor_d_pago = (
            "#yield-distribuition > div > div.content--info > div:nth-child(2) > span.content--info--item--value.amount"
        )
        conteudo_d_pago = self._page.locator(seletor_d_pago).text_content()

        if not conteudo_d_pago:
            raise ElementoNaoEncontradoError(seletor=seletor_d_pago)

        dividendo_pago = conteudo_d_pago.strip()

        return (dividend_yield, dividendo_pago)

    def obter_dividend_yield_6_meses(self) -> tuple[str, str]:
        seletor_dy = "#yield-distribuition > div > div.content--info > div:nth-child(3) > span.content--info--item--value:not(.amount)"
        conteudo_dy = self._page.locator(seletor_dy).text_content()

        if not conteudo_dy:
            raise ElementoNaoEncontradoError(seletor=seletor_dy)
        dividend_yield = conteudo_dy.strip()

        seletor_d_pago = (
            "#yield-distribuition > div > div.content--info > div:nth-child(3) > span.content--info--item--value.amount"
        )
        conteudo_d_pago = self._page.locator(seletor_d_pago).text_content()

        if not conteudo_d_pago:
            raise ElementoNaoEncontradoError(seletor=seletor_d_pago)

        dividendo_pago = conteudo_d_pago.strip()

        return (dividend_yield, dividendo_pago)

    def obter_dividend_yield_12_meses(self) -> tuple[str, str]:
        seletor_dy = "#yield-distribuition > div > div.content--info > div:nth-child(4) > span.content--info--item--value:not(.amount)"
        conteudo_dy = self._page.locator(seletor_dy).text_content()

        if not conteudo_dy:
            raise ElementoNaoEncontradoError(seletor=seletor_dy)
        dividend_yield = conteudo_dy.strip()

        seletor_d_pago = (
            "#yield-distribuition > div > div.content--info > div:nth-child(4) > span.content--info--item--value.amount"
        )
        conteudo_d_pago = self._page.locator(seletor_d_pago).text_content()

        if not conteudo_d_pago:
            raise ElementoNaoEncontradoError(seletor=seletor_d_pago)

        dividendo_pago = conteudo_d_pago.strip()

        return (dividend_yield, dividendo_pago)

    def obter_segmento(self) -> str:
        return self.__obter_valor_de_informacoes_da_empresa("segmento")

    def obter_tipo_de_fundo(self) -> str:
        return self.__obter_valor_de_informacoes_da_empresa("TIPO DE FUNDO")

    def obter_pvp(self) -> str:
        seletor = "#cards-ticker > div._card.vp > div._card-body > span"
        pvp = self._page.locator(seletor).text_content()

        if not pvp:
            raise ElementoNaoEncontradoError(seletor=seletor)
        return pvp.strip()

    def obter_quantidade_cotas_emitidas(self) -> str:
        return self.__obter_valor_de_informacoes_da_empresa("COTAS EMITIDAS")

    def obter_valor_patrimonial_por_cota(self) -> str:
        return self.__obter_valor_de_informacoes_da_empresa("VAL. PATRIMONIAL P/ COTA")

    def __scrape_informacoes_sobre_empresa(self) -> list[Locator]:
        informacoes = self._page.locator("#table-indicators > div")

        return [informacoes.nth(i) for i in range(informacoes.count())]

    def __obter_valor_de_informacoes_da_empresa(self, tipo_informacao: str) -> str:
        informacoes_sobre_empresa = self.__scrape_informacoes_sobre_empresa()

        for elemento in informacoes_sobre_empresa:
            if str(elemento.locator("div.desc > span").text_content()).strip().lower() == tipo_informacao.lower():
                info = elemento.locator("div.desc > div > span").text_content() or ""
                return info.strip()

        raise ElementoNaoEncontradoError(seletor=tipo_informacao.upper())
