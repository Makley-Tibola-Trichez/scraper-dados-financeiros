from logging import Logger
from sqlite3 import Connection
from typing import Any

from ..models.fii import FiiModel


class FiiRepository:
    def __init__(self, conn: Connection, logger: Logger) -> None:
        self.conn = conn
        self._logger = logger

    def __sql_para_fii(self, row: tuple[Any, ...]) -> FiiModel:
        return FiiModel(
            id=row[0],
            ticker=row[1],
            tipo_de_fundo=row[2],
            segmento=row[3],
            cotacao=row[4],
            pvp=row[5],
            quantidade_cotas_emitidas=row[6],
            valor_patrimonial_por_cota=row[7],
            dividendo_1_mes=row[8],
            dividendo_3_meses=row[9],
            dividendo_6_meses=row[10],
            dividendo_12_meses=row[11],
            dividend_yield_1_mes=row[12],
            dividend_yield_3_meses=row[13],
            dividend_yield_6_meses=row[14],
            dividend_yield_12_meses=row[15],
            date=row[16],
        )

    def verificar_se_existem_tickers(self, tickers: list[Any], date: str) -> list[tuple[str, FiiModel | None]]:
        cursor = self.conn.cursor()

        placeholders = ",".join("?" * len(tickers))

        self._logger.info(f"Verificando existência de FIIs no banco de dados para a data {date} e tickers: {tickers}")
        cursor.execute(
            f"""
            SELECT *
            FROM fiis
            WHERE date = ?
            AND ticker in ({placeholders})
        """,  # noqa: S608 Está inserindo a quantidade necessária de parâmetros, não há risco de SQL Injection.
            (date, *tickers),
        )

        fiis: list[tuple[str, FiiModel | None]] = []

        results = [self.__sql_para_fii(row) for row in cursor.fetchall()]
        cursor.close()

        for ticker in tickers:
            if any(fii.ticker == ticker for fii in results):
                self._logger.info(f"FII {ticker} encontrado no banco de dados para a data {date}")
                fii = next(fii for fii in results if fii.ticker == ticker)
                fiis.append((ticker, fii))
            else:
                self._logger.info(f"FII {ticker} não encontrado no banco de dados para a data {date}")
                fiis.append((ticker, None))

        return fiis

    def inserir(self, fii: FiiModel) -> FiiModel:
        cursor = self.conn.cursor()

        self._logger.info(f"Inserindo FII {fii.ticker} no banco de dados")
        cursor = cursor.execute(
            """
            INSERT INTO fiis (
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
                dividendo_12_meses
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING *
            """,
            (
                fii.ticker,
                fii.tipo_de_fundo,
                fii.segmento,
                fii.cotacao,
                fii.pvp,
                fii.quantidade_cotas_emitidas,
                fii.valor_patrimonial_por_cota,
                fii.dividendo_1_mes,
                fii.dividendo_3_meses,
                fii.dividendo_6_meses,
                fii.dividendo_12_meses,
                fii.dividend_yield_1_mes,
                fii.dividend_yield_3_meses,
                fii.dividend_yield_6_meses,
                fii.dividend_yield_12_meses,
            ),
        )

        (
            id,
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
            date,
        ) = cursor.fetchone()

        self.conn.commit()
        cursor.close()

        return FiiModel(
            id,
            ticker,
            tipo_de_fundo,
            segmento,
            cotacao,
            pvp,
            quantidade_cotas_emitidas,
            valor_patrimonial_por_cota,
            dividendo_1_mes,
            dividendo_3_meses,
            dividendo_6_meses,
            dividendo_12_meses,
            dividend_yield_1_mes,
            dividend_yield_3_meses,
            dividend_yield_6_meses,
            dividend_yield_12_meses,
            date=date,
        )

    def existe(self, ticker: str, date: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT 1 FROM fiis
            WHERE ticker = ? AND date = ?
            """,
            (ticker, date),
        )
        existe = cursor.fetchone() is not None

        cursor.close()
        return existe
