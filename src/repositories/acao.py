

from sqlite3 import Connection
from src.models.acao import AcaoModel


class AcaoRepository:
    def __init__(self, conn: Connection) -> None:
        self.conn = conn
        
    def inserir(self, acao: AcaoModel):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO acoes (ticker, cotacao, pl, pvp, dividend_yield, payout)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (acao.ticker, acao.cotacao, acao.pl, acao.pvp, acao.dividend_yield, acao.payout))
        self.conn.commit()
    
    def obter_por_ticker_e_data(self, ticker: str, date: str) -> AcaoModel | None:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM acoes
            WHERE ticker = ? AND date = ?
        ''', (ticker, date))
        
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
        )
    

    def existe(self, ticker: str, date: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT 1 FROM acoes
            WHERE ticker = ? AND date = ?
        ''', (ticker, date))
        
        return cursor.fetchone() is not None
    
    
