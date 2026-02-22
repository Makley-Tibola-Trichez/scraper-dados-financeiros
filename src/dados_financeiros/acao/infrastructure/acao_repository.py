from datetime import datetime
import json
from logging import Logger
from sqlite3 import Connection
from typing import Any

from dados_financeiros.acao.domain.interfaces import IAcaoRepository
from dados_financeiros.acao.domain.value_objects import Acao, Dividendo


class AcaoRepository(IAcaoRepository):
    def __init__(self, conn: Connection, logger: Logger) -> None:
        self.conn = conn
        self._logger = logger

    def _sql_to_acao(self, row: tuple[Any, ...]) -> Acao:
        dividendos: list[Dividendo] = []

        try:
            dividendos = [Dividendo(**r) for r in json.loads(row[21])]
        except Exception as _:
            self._logger.warning("Nenhum dividendo encontrado")

        return Acao(
            ticker=row[1],
            cotacao=row[2],
            pl=row[3],
            pvp=row[4],
            vpa=row[10],
            lpa=row[11],
            roe=row[12],
            dy=row[5],
            payout=row[6],
            setor=row[8],
            segmento=row[9],
            roa=row[13],
            roic=row[14],
            cagr_lucros_5_anos=row[15],
            cagr_receitas_5_anos=row[16],
            db_patrimonio=row[17],
            dl_ebit=row[18],
            dl_ebitda=row[19],
            dl_patrimonio=row[20],
            dividendos=dividendos,
        )

    def obter_tickers_existentes(self, tickers: list[str], date: datetime) -> list[tuple[str, Acao | None]]:
        cursor = self.conn.cursor()

        placeholders = ",".join("?" * len(tickers))

        cursor.execute(
            f"""
            SELECT
                *
            FROM
                acao AS a
            WHERE
                date = ?
            AND
                ticker in ({placeholders})
        """,  # noqa: S608 Está inserindo a quantidade necessária de parâmetros, não há risco de SQL Injection.
            (date.date(), *tickers),
        )

        acoes: list[tuple[str, Acao | None]] = []

        results = [self._sql_to_acao(row) for row in cursor.fetchall()]
        cursor.close()

        for ticker in tickers:
            if any(acao.ticker == ticker for acao in results):
                acao = next(acao for acao in results if acao.ticker == ticker)
                acoes.append((ticker, acao))
            else:
                acoes.append((ticker, None))

        return acoes

    def inserir(self, acao: Acao) -> Acao:
        cursor = self.conn.cursor()
        cursor = cursor.execute(
            """
            INSERT INTO acao (
                ticker,
                cotacao,
                pl,
                pvp,
                vpa,
                lpa,
                roe,
                dy,
                payout,
                setor,
                segmento,
                roa,
                roic,
                cagr_lucros_5_anos,
                cagr_receitas_5_anos,
                db_patrimonio,
                dl_patrimonio,
                dl_ebitda,
                dl_ebit
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING *
        """,
            (
                acao.ticker,
                acao.cotacao,
                acao.pl,
                acao.pvp,
                acao.vpa,
                acao.lpa,
                acao.roe,
                acao.dy,
                acao.payout,
                acao.setor,
                acao.segmento,
                acao.roa,
                acao.roic,
                acao.cagr_lucros_5_anos,
                acao.cagr_receitas_5_anos,
                acao.db_patrimonio,
                acao.dl_patrimonio,
                acao.dl_ebitda,
                acao.dl_ebit,
            ),
        )
        novo_registro = cursor.fetchone()
        self.conn.commit()
        dividendos: list[tuple] = []

        for div in acao.dividendos:
            dividendos.append((acao.ticker, div.valor, div.data_anuncio, div.data_pagamento, div.tipo))

        # print(dividendos)

        # cursor = cursor.executemany(
        #     """
        #     INSERT INTO acao_historico_dividendos (
        #         ticker,
        #         valor,
        #         data_anuncio,
        #         data_pagamento,
        #         tipo
        #     )
        #     VALUES (?, ?, ?, ?, ?)
        #     RETURNING *
        # """,
        #     dividendos,
        # )

        # dividendos = cursor.fetchall()
        # self.conn.commit()
        cursor.close()

        # print(dividendos)

        # input("dividendos")

        acao = self._sql_to_acao((*novo_registro,))

        return acao

    def obter_por_ticker_e_data(self, ticker: str, date: str) -> Acao | None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM acao
            WHERE ticker = ? AND date = ?
        """,
            (ticker, date),
        )

        dados_acao = cursor.fetchone()
        cursor.close()
        if not dados_acao:
            return None

        acao = self._sql_to_acao(dados_acao)

        return acao

    def existe(self, ticker: str, date: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT 1 FROM acao
            WHERE ticker = ? AND date = ?
        """,
            (ticker, date),
        )

        existe = cursor.fetchone() is not None

        cursor.close()
        return existe
