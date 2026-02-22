from logging import Logger
from sqlite3 import Connection

from dados_financeiros.fii.domain.interfaces import IFiiRepository
from dados_financeiros.fii.domain.value_objects import Fii


class FiiRepository(IFiiRepository):
    def __init__(self, conn: Connection, logger: Logger) -> None:
        self._conn = conn
        self._logger = logger

    @staticmethod
    def _to_str(value: object | None) -> str:
        if value is None:
            return ""
        return str(value)

    def _sql_to_fii(self, row: tuple[object, ...]) -> Fii:
        return Fii(
            ticker=self._to_str(row[1]),
            tipo_de_fundo=self._to_str(row[2]),
            segmento=self._to_str(row[3]),
            cotacao=self._to_str(row[4]),
            pvp=self._to_str(row[5]),
            quantidade_cotas_emitidas=self._to_str(row[6]),
            valor_patrimonial_por_cota=self._to_str(row[7]),
            dividend_yield_1_mes=self._to_str(row[8]),
            dividend_yield_3_meses=self._to_str(row[9]),
            dividend_yield_6_meses=self._to_str(row[10]),
            dividend_yield_12_meses=self._to_str(row[11]),
            dividendo_1_mes=self._to_str(row[12]),
            dividendo_3_meses=self._to_str(row[13]),
            dividendo_6_meses=self._to_str(row[14]),
            dividendo_12_meses=self._to_str(row[15]),
        )

    def obter_tickers_existentes(self, tickers: list[str], date: str) -> list[tuple[str, Fii | None]]:
        if len(tickers) == 0:
            return []

        cursor = self._conn.cursor()
        placeholders = ",".join("?" * len(tickers))

        self._logger.info(f"Verificando existência de FIIs no banco de dados para a data {date}")
        cursor.execute(
            f"""
            SELECT *
            FROM fii
            WHERE date = ?
            AND ticker in ({placeholders})
        """,  # noqa: S608 EstÃ¡ inserindo apenas placeholders para query parametrizada.
            (date, *tickers),
        )

        results = [self._sql_to_fii(row) for row in cursor.fetchall()]
        cursor.close()

        fiis: list[tuple[str, Fii | None]] = []
        for ticker in tickers:
            if any(fii.ticker == ticker for fii in results):
                fii = next(fii for fii in results if fii.ticker == ticker)
                fiis.append((ticker, fii))
            else:
                fiis.append((ticker, None))

        return fiis

    def inserir(self, fii: Fii) -> Fii:
        cursor = self._conn.cursor()
        cursor = cursor.execute(
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
                fii.dividend_yield_1_mes,
                fii.dividend_yield_3_meses,
                fii.dividend_yield_6_meses,
                fii.dividend_yield_12_meses,
                fii.dividendo_1_mes,
                fii.dividendo_3_meses,
                fii.dividendo_6_meses,
                fii.dividendo_12_meses,
            ),
        )

        novo_registro = cursor.fetchone()
        self._conn.commit()
        cursor.close()

        return self._sql_to_fii((*novo_registro,))
