

from sqlite3 import Connection
from src.models.acao import AcaoModel
from src.models.dividendo import DividendoAnualModel


    
def obter_acao_db(connection: Connection, ticker: str) -> AcaoModel | None:
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM acoes
        WHERE ticker = ? AND date = DATE('now')
    ''', (ticker,))
    
    dados_acao = cursor.fetchone()
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
        segmento=dados_acao[9]
    )

def inserir_acao_db(connection: Connection, acao: AcaoModel):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO acoes (ticker, cotacao, pl, pvp, dividend_yield, payout)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (acao.ticker, acao.cotacao, acao.pl, acao.pvp, acao.dividend_yield, acao.payout))
    connection.commit()
    
def inserir_dividendos_anuais_db(connection: Connection, dividendos: list[DividendoAnualModel]):
    cursor = connection.cursor()
    for dividendo in dividendos:
        dados_dividendo = (dividendo.ticker, dividendo.ano, dividendo.valor)
        cursor.execute('''
            INSERT INTO dividendos_anuais (ticker, ano, valor)
            SELECT ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM dividendos_anuais
                WHERE ticker = ? AND ano = ? AND valor = ?
            )
        ''', (*dados_dividendo, *dados_dividendo))
        connection.commit()

def obter_dividendos_anuais_db(connection: Connection, ticker: str) -> list[tuple[str, str, float]]:
    cursor = connection.cursor()
    cursor.execute('''
        SELECT ticker, ano, valor FROM dividendos_anuais
        WHERE ticker = ?
    ''', (ticker,))
    
    return cursor.fetchall()