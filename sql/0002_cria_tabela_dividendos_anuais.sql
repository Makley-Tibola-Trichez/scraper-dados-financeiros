-- sql/0002_cria_tabela_dividendos_anuais.sql
CREATE TABLE IF NOT EXISTS dividendos_anuais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT,
    ano INTEGER,
    valor REAL,
    date TEXT DEFAULT CURRENT_DATE,
    FOREIGN KEY (ticker) REFERENCES acoes(ticker)
)
