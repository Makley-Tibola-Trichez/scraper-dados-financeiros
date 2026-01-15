from datetime import datetime, timezone
from sqlite3 import Connection, IntegrityError

from ..models.dividendo import DividendoHistoricoModel


class DividendoHistoricoRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def __sql_to_model(self, row: tuple) -> DividendoHistoricoModel:
        ticker, valor, data_anuncio, data_pagamento, tipo, data = row

        data_pagamento_tratada = None
        if data_pagamento is not None:
            data_pagamento_tratada = datetime.fromisoformat(data_pagamento)

        return DividendoHistoricoModel(
            ticker=ticker,
            data=data,
            data_anuncio=datetime.fromisoformat(data_anuncio).replace(tzinfo=timezone.utc),
            data_pagamento=data_pagamento_tratada,
            tipo=tipo,
            valor=valor,
        )

    def inserir(self, dividendos: list[DividendoHistoricoModel]) -> list[DividendoHistoricoModel]:
        """
        Insere vários dividendos de uma vez usando executemany.
        Depois executa um SELECT eficiente para retornar todos os registros
        (convertidos para model).
        """

        cursor = self.conn.cursor()

        # Prepara os valores
        valores = [
            (
                d.ticker,
                d.valor,
                d.data_anuncio.isoformat(),
                d.data_pagamento.isoformat() if d.data_pagamento else None,
                d.tipo,
            )
            for d in dividendos
        ]

        try:
            # Inserção em lote
            cursor.executemany(
                """
                INSERT INTO dividendos_historico
                    (ticker, valor, data_anuncio, data_pagamento, tipo)
                VALUES (?, ?, ?, ?, ?)
                """,
                valores,
            )
            self.conn.commit()
        except IntegrityError:
            # Mesmo comportamento da sua versão original: retornar todos já enviados
            return dividendos

        # Agora buscamos todos os registros inseridos de uma vez
        # — rápido, pois busca apenas tickers da lista
        tickers = tuple(d.ticker for d in dividendos)

        cursor.execute(
            f"""
            SELECT *
            FROM dividendos_historico
            WHERE ticker IN ({",".join(["?"] * len(tickers))})
            ORDER BY data_anuncio
            """,  # noqa: S608 Está inserindo a quantidade necessária de parâmetros, não há risco de SQL Injection.
            tickers,
        )

        rows = cursor.fetchall()
        return [self.__sql_to_model(row) for row in rows]
