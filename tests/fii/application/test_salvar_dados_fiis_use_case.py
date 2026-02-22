import logging
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from dados_financeiros.fii.application.salvar_dados_fiis_use_case import SalvarFiiUseCase  # noqa: E402
from dados_financeiros.fii.domain.value_objects import Fii  # noqa: E402


def make_fii(ticker: str) -> Fii:
    return Fii(
        ticker=ticker,
        tipo_de_fundo="FUNDO DE PAPEL",
        segmento="TITULOS E VALORES MOBILIARIOS",
        cotacao="R$ 100,00",
        pvp="0,95",
        quantidade_cotas_emitidas="100000",
        valor_patrimonial_por_cota="R$ 102,00",
        dividendo_1_mes="R$ 1,00",
        dividendo_3_meses="R$ 3,00",
        dividendo_6_meses="R$ 6,00",
        dividendo_12_meses="R$ 12,00",
        dividend_yield_1_mes="1,00%",
        dividend_yield_3_meses="3,00%",
        dividend_yield_6_meses="6,00%",
        dividend_yield_12_meses="12,00%",
    )


class FakeGateway:
    def __init__(self, fiis: dict[str, Fii], failure_tickers: set[str] | None = None) -> None:
        self._fiis = fiis
        self._failure_tickers = failure_tickers or set()
        self.calls: list[str] = []

    def fechar(self) -> None:
        return None

    def obter_dados(self, ticker: str) -> Fii:
        self.calls.append(ticker)
        if ticker in self._failure_tickers:
            raise RuntimeError("gateway error")
        return self._fiis[ticker]


class FakeRepository:
    def __init__(self, existentes: dict[str, Fii | None] | None = None) -> None:
        self._existentes = existentes or {}
        self.inserted: list[Fii] = []
        self.queries: list[tuple[list[str], str]] = []

    def inserir(self, fii: Fii) -> Fii:
        self.inserted.append(fii)
        return fii

    def obter_tickers_existentes(self, tickers: list[str], date: str) -> list[tuple[str, Fii | None]]:
        self.queries.append((tickers, date))
        return [(ticker, self._existentes.get(ticker)) for ticker in tickers]


class SalvarFiiUseCaseTest(unittest.TestCase):
    def test_retorna_existentes_sem_inserir(self) -> None:
        fii_existente = make_fii("HGLG11")
        gateway = FakeGateway({})
        repository = FakeRepository({"HGLG11": fii_existente})
        use_case = SalvarFiiUseCase(logging.getLogger("test"), gateway, repository)

        resultado = use_case.executar(["HGLG11"])

        self.assertEqual(resultado, [fii_existente])
        self.assertEqual(repository.inserted, [])
        self.assertEqual(gateway.calls, [])

    def test_scrape_e_insercao_quando_ticker_nao_existe(self) -> None:
        fii_novo = make_fii("KNRI11")
        gateway = FakeGateway({"KNRI11": fii_novo})
        repository = FakeRepository()
        use_case = SalvarFiiUseCase(logging.getLogger("test"), gateway, repository)

        resultado = use_case.executar(["KNRI11"])

        self.assertEqual(resultado, [fii_novo])
        self.assertEqual(gateway.calls, ["KNRI11"])
        self.assertEqual(repository.inserted, [fii_novo])

    def test_falha_rapido_quando_gateway_lanca_erro(self) -> None:
        gateway = FakeGateway({}, failure_tickers={"FAIL11"})
        repository = FakeRepository()
        use_case = SalvarFiiUseCase(logging.getLogger("test"), gateway, repository)

        with self.assertRaises(SystemExit):
            use_case.executar(["FAIL11", "NEXT11"])

        self.assertEqual(gateway.calls, ["FAIL11"])
        self.assertEqual(repository.inserted, [])
