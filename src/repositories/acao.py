from sqlite3 import Connection
from typing import Any

from ..models.acao import AcaoModel


class AcaoRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def __sql_to_acao(self, row: tuple[Any, ...]) -> AcaoModel:
        return AcaoModel(
            id=row[0],
            ticker=row[1],
            cotacao=row[2],
            pl=row[3],
            pvp=row[4],
            dividend_yield=row[5],
            payout=row[6],
            date=row[7],
            setor=row[8],
            segmento=row[9],
            vpa=row[10],
            lpa=row[11],
            roe=row[12],
        )

    def verificar_se_existem_tickers(self, tickers: list[Any], date: str) -> list[tuple[str, AcaoModel | None]]:
        cursor = self.conn.cursor()

        placeholders = ",".join("?" * len(tickers))

        cursor.execute(
            f"""
            SELECT *
            FROM acoes
            WHERE date = ?
            AND ticker in ({placeholders})
        """,  # noqa: S608 Está inserindo a quantidade necessária de parâmetros, não há risco de SQL Injection.
            (date, *tickers),
        )

        acoes: list[tuple[str, AcaoModel | None]] = []

        results = [self.__sql_to_acao(row) for row in cursor.fetchall()]
        cursor.close()

        for ticker in tickers:
            if any(acao.ticker == ticker for acao in results):
                acao = next(acao for acao in results if acao.ticker == ticker)
                acoes.append((ticker, acao))
            else:
                acoes.append((ticker, None))

        return acoes

    def inserir(self, acao: AcaoModel) -> AcaoModel:
        cursor = self.conn.cursor()
        cursor = cursor.execute(
            """
            INSERT INTO acoes (
                ticker,
                cotacao,
                pl,
                pvp,
                vpa,
                lpa,
                roe,
                dividend_yield,
                payout,
                setor,
                segmento
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                acao.dividend_yield,
                acao.payout,
                acao.setor,
                acao.segmento,
            ),
        )

        id, ticker, cotacao, pl, pvp, dividend_yield, payout, date, setor, segmento, vpa, lpa, roe = cursor.fetchone()

        self.conn.commit()
        cursor.close()
        acao = AcaoModel(
            id=id,
            ticker=ticker,
            cotacao=cotacao,
            pl=pl,
            pvp=pvp,
            vpa=vpa,
            lpa=lpa,
            roe=roe,
            dividend_yield=dividend_yield,
            payout=payout,
            setor=setor,
            segmento=segmento,
            date=date,
        )

        return acao

    def obter_por_ticker_e_data(self, ticker: str, date: str) -> AcaoModel | None:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM acoes
            WHERE ticker = ? AND date = ?
        """,
            (ticker, date),
        )

        dados_acao = cursor.fetchone()
        cursor.close()
        if not dados_acao:
            return None

        return AcaoModel(
            id=dados_acao[0],
            ticker=dados_acao[1],
            cotacao=dados_acao[2],
            pl=dados_acao[3],
            pvp=dados_acao[4],
            dividend_yield=dados_acao[5],
            payout=dados_acao[6],
            date=dados_acao[7],
            setor=dados_acao[8],
            segmento=dados_acao[9],
            vpa=dados_acao[10],
            lpa=dados_acao[11],
            roe=dados_acao[12],
        )

    def existe(self, ticker: str, date: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT 1 FROM acoes
            WHERE ticker = ? AND date = ?
        """,
            (ticker, date),
        )

        existe = cursor.fetchone() is not None

        cursor.close()
        return existe
