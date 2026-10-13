import logging
import sys
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from dados_financeiros.acao.application.salvar_dados_acoes_use_case import SalvarAcaoUseCase  # noqa: E402
from dados_financeiros.acao.domain.value_objects import Acao  # noqa: E402


def make_acao(ticker: str) -> Acao:
    return Acao(
        ticker=ticker,
        cotacao=10.0,
        pl="10",
        pvp="1,00",
        lpa="1,00",
        dy="5,00%",
        roe="15,00%",
        roic="10,00%",
        roa="10,00%",
        vpa="10,00",
        payout="50,00%",
        setor="SETOR",
        segmento="SEGMENTO",
        dl_patrimonio="0,5",
        dl_ebitda="1,0",
        dl_ebit="1,0",
        db_patrimonio="0,5",
        cagr_receitas_5_anos="10,00%",
        cagr_lucros_5_anos="10,00%",
        dividendos=[],
    )


class FakeGateway:
    def __init__(self, acoes: dict[str, Acao], failure_tickers: set[str] | None = None) -> None:
        self._acoes = acoes
        self._failure_tickers = failure_tickers or set()
        self.calls: list[str] = []

    def fechar(self) -> None:
        return None

    def obter_dados(self, ticker: str) -> Acao:
        self.calls.append(ticker)
        if ticker in self._failure_tickers:
            raise RuntimeError("gateway error")
        return self._acoes[ticker]

    def obter_dividendos(self, ticker: str) -> list:
        return []


class FakeRepository:
    def __init__(self, existentes: dict[str, Acao | None] | None = None) -> None:
        self._existentes = existentes or {}
        self.inserted: list[Acao] = []
        self.queries: list[tuple[list[str], datetime]] = []

    def inserir(self, acao: Acao) -> Acao:
        self.inserted.append(acao)
        return acao

    def obter_tickers_existentes(self, tickers: list[str], date: datetime) -> list[tuple[str, Acao | None]]:
        self.queries.append((tickers, date))
        return [(ticker, self._existentes.get(ticker)) for ticker in tickers]


class SalvarAcaoUseCaseTest(unittest.TestCase):
    def test_retorna_existentes_sem_inserir(self) -> None:
        acao_existente = make_acao("ITSA4")
        gateway = FakeGateway({})
        repository = FakeRepository({"ITSA4": acao_existente})
        use_case = SalvarAcaoUseCase(logging.getLogger("test"), gateway, repository)

        resultado = use_case.executar(["ITSA4"])

        self.assertEqual(resultado, [acao_existente])
        self.assertEqual(repository.inserted, [])
        self.assertEqual(gateway.calls, [])

    def test_scrape_e_insercao_quando_ticker_nao_existe(self) -> None:
        acao_nova = make_acao("BBAS3")
        gateway = FakeGateway({"BBAS3": acao_nova})
        repository = FakeRepository()
        use_case = SalvarAcaoUseCase(logging.getLogger("test"), gateway, repository)

        resultado = use_case.executar(["BBAS3"])

        self.assertEqual(resultado, [acao_nova])
        self.assertEqual(gateway.calls, ["BBAS3"])
        self.assertEqual(repository.inserted, [acao_nova])

    def test_continua_para_proximo_ticker_quando_gateway_lanca_erro(self) -> None:
        acao_nova = make_acao("NEXT3")
        gateway = FakeGateway({"NEXT3": acao_nova}, failure_tickers={"FAIL3"})
        repository = FakeRepository()
        use_case = SalvarAcaoUseCase(logging.getLogger("test"), gateway, repository)

        resultado = use_case.executar(["FAIL3", "NEXT3"])

        self.assertEqual(gateway.calls, ["FAIL3", "NEXT3"])
        self.assertEqual(resultado, [acao_nova])
        self.assertEqual(repository.inserted, [acao_nova])


if __name__ == "__main__":
    unittest.main()
