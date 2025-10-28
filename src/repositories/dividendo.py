

from sqlite3 import Connection

from src.models.acao import AcaoModel
from src.models.dividendo import DividendoModel


class DividendoRepository:
    
    def __init__(self, conn: Connection):
        self.conn = conn
        
    def inserir(self, dividendo: DividendoModel):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO dividendos_anuais (ticker, ano, valor)
            SELECT ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM dividendos_anuais
                WHERE ticker = ? AND ano = ? AND valor = ?
            )
        ''', (dividendo.ticker, dividendo.ano, dividendo.valor,
              dividendo.ticker, dividendo.ano, dividendo.valor))
        self.conn.commit()
    
    def inserir_anuais(self, dividendos: list[DividendoModel]):
        cursor = self.conn.cursor()
        for dividendo in dividendos:
            valor = (dividendo.ticker, dividendo.ano, dividendo.valor)
            cursor.execute('''
                INSERT INTO dividendos_anuais (ticker, ano, valor)
                SELECT ?, ?, ?
                WHERE NOT EXISTS (
                    SELECT 1 FROM dividendos_anuais
                    WHERE ticker = ? AND ano = ? AND valor = ?
                )
            ''', (*valor, *valor))
        self.conn.commit()
    
    def obter_por_ticker(self, ticker: str) -> list[DividendoModel] | None:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, ticker, ano, valor, date FROM dividendos_anuais
            WHERE ticker = ?
            ORDER BY ano DESC
            LIMIT 4
        ''', (ticker,))
        
        valores = cursor.fetchall()
        
        if not valores:
            return None
        
        return [DividendoModel(id=v[0], ticker=v[1],ano=v[2], valor=v[3], date=v[4]) for v in valores]
        
        
    
    def exists(self, ticker: str, ano: str, valor: float) -> bool:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT 1 FROM dividendos_anuais
            WHERE ticker = ? AND ano = ? AND valor = ?
        ''', (ticker, ano, valor))
        
        return cursor.fetchone() is not None