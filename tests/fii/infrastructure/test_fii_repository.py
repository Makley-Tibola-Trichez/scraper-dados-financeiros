import logging
import sqlite3
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from dados_financeiros.fii.domain.value_objects import Fii  # noqa: E402
from dados_financeiros.fii.infrastructure.fii_repository import FiiRepository  # noqa: E402


def make_fii(ticker: str) -> Fii:
    return Fii(
        ticker=ticker,
        tipo_de_fundo="FUNDO DE PAPEL",
        segmento="TITULOS E VALORES MOBILIARIOS",
        cotacao="R$ 100,00",
        pvp="0,95",
        quantidade_cotas_emitidas="100000",
        valor_patrimonial_por_cota="R$ 102,00",
        dividendo_1_mes="R$ 1,50",
        dividendo_3_meses="R$ 4,50",
        dividendo_6_meses="R$ 9,00",
        dividendo_12_meses="R$ 18,00",
        dividend_yield_1_mes="0,90%",
        dividend_yield_3_meses="2,70%",
        dividend_yield_6_meses="5,40%",
        dividend_yield_12_meses="10,80%",
    )


def criar_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE fii (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            tipo_de_fundo TEXT,
            segmento TEXT,
            cotacao REAL,
            pvp REAL,
            quantidade_cotas_emitidas REAL,
            valor_patrimonial_por_cota REAL,
            dividend_yield_1_mes REAL,
            dividend_yield_3_meses REAL,
            dividend_yield_6_meses REAL,
            dividend_yield_12_meses REAL,
            dividendo_1_mes REAL,
            dividendo_3_meses REAL,
            dividendo_6_meses REAL,
            dividendo_12_meses REAL,
            date TEXT DEFAULT CURRENT_DATE
        )
        """
    )
    conn.commit()


def inserir_linha(conn: sqlite3.Connection, fii: Fii, date: str) -> None:
    conn.execute(
        """
        INSERT INTO fii (
            ticker,
            tipo_de_fundo,
            segmento,
            cotacao,
            pvp,
            quantidade_cotas_emitidas,
            valor_patrimonial_por_cota,
            dividend_yield_1_mes,
            dividend_yield_3_meses,
            dividend_yield_6_meses,
            dividend_yield_12_meses,
            dividendo_1_mes,
            dividendo_3_meses,
            dividendo_6_meses,
            dividendo_12_meses,
            date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            fii.ticker,
            fii.tipo_de_fundo,
            fii.segmento,
            fii.cotacao,
            fii.pvp,
            fii.quantidade_cotas_emitidas,
            fii.valor_patrimonial_por_cota,
            fii.dividend_yield_1_mes,
            fii.dividend_yield_3_meses,
            fii.dividend_yield_6_meses,
            fii.dividend_yield_12_meses,
            fii.dividendo_1_mes,
            fii.dividendo_3_meses,
            fii.dividendo_6_meses,
            fii.dividendo_12_meses,
            date,
        ),
    )
    conn.commit()


class FiiRepositoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.conn = sqlite3.connect(":memory:")
        criar_schema(self.conn)
        self.repository = FiiRepository(self.conn, logging.getLogger("test"))

    def tearDown(self) -> None:
        self.conn.close()

    def test_inserir_persiste_e_mapeia_campos_corretamente(self) -> None:
        fii = make_fii("HGLG11")

        criado = self.repository.inserir(fii)
        row = self.conn.execute(
            "SELECT dividend_yield_1_mes, dividendo_1_mes FROM fii WHERE ticker = ?",
            ("HGLG11",),
        ).fetchone()

        self.assertIsNotNone(row)
        self.assertEqual(criado.dividend_yield_1_mes, "0,90%")
        self.assertEqual(criado.dividendo_1_mes, "R$ 1,50")
        self.assertEqual(row, ("0,90%", "R$ 1,50"))

    def test_obter_tickers_existentes_respeita_ordem_e_data(self) -> None:
        inserir_linha(self.conn, make_fii("A11"), "2026-02-22")
        inserir_linha(self.conn, make_fii("B11"), "2026-02-21")
        inserir_linha(self.conn, make_fii("C11"), "2026-02-22")

        resultado = self.repository.obter_tickers_existentes(["B11", "A11", "C11"], "2026-02-22")

        self.assertEqual([ticker for ticker, _ in resultado], ["B11", "A11", "C11"])
        self.assertIsNone(resultado[0][1])
        self.assertEqual(resultado[1][1].ticker if resultado[1][1] else None, "A11")
        self.assertEqual(resultado[2][1].ticker if resultado[2][1] else None, "C11")

    def test_obter_tickers_existentes_retorna_none_para_ticker_ausente(self) -> None:
        inserir_linha(self.conn, make_fii("A11"), "2026-02-22")

        resultado = self.repository.obter_tickers_existentes(["A11", "X11"], "2026-02-22")

        self.assertEqual(resultado[0][0], "A11")
        self.assertIsNotNone(resultado[0][1])
        self.assertEqual(resultado[1], ("X11", None))

    def test_obter_tickers_existentes_com_lista_vazia_retorna_lista_vazia(self) -> None:
        resultado = self.repository.obter_tickers_existentes([], "2026-02-22")

        self.assertEqual(resultado, [])
