from sqlite3 import Connection, IntegrityError
from src.models.dividendo import DividendoHistoricoModel
from datetime import datetime 

class DividendoHistoricoRepository:
    
    def __init__(self, conn: Connection) -> None:
        self.conn = conn
        
    def inserir(self, dividendo: DividendoHistoricoModel):
        cursor = self.conn.cursor()
        
        
        try:
            
            cursor = cursor.execute('''
                INSERT INTO dividendos_historico (ticker, valor, data_anuncio, data_pagamento, tipo)
                VALUES (?, ?, ?, ?, ?)
                RETURNING *
            ''', (
                dividendo.ticker, 
                dividendo.valor, 
                dividendo.data_anuncio.isoformat(), 
                dividendo.data_pagamento.isoformat() if dividendo.data_pagamento is not None else None,
                dividendo.tipo
            ))
            ticker, valor, data_anuncio, data_pagamento, tipo, data = cursor.fetchone()
            self.conn.commit()
                
            data_pagamento_tratada = None
            if data_pagamento is not None:
                data_pagamento_tratada = datetime.fromisoformat(data_pagamento)
            
            return DividendoHistoricoModel(
                ticker=ticker,
                data=data,
                data_anuncio=datetime.fromisoformat(data_anuncio),
                data_pagamento=data_pagamento_tratada,
                tipo=tipo,
                valor=valor
            )
        except IntegrityError as _e:
            return dividendo
            
    
        
    