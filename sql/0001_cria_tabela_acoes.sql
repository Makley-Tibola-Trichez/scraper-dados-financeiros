-- sql/0001_cria_tabela_acoes.sql
CREATE TABLE IF NOT EXISTS acoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT,
    cotacao REAL,
    pl REAL,
    pvp REAL,
    dividend_yield REAL,
    payout REAL,
    date TEXT DEFAULT CURRENT_DATE
)
