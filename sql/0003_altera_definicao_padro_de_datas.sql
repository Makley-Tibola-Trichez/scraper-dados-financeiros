-- sql/0003_altera_definicao_padro_de_datas.sql
PRAGMA foreign_keys=off;
BEGIN TRANSACTION;
DROP TABLE dividendos_anuais;

CREATE TABLE IF NOT EXISTS dividendos_anuais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT,
    ano INTEGER,
    valor REAL,
    date TEXT DEFAULT (date('now', 'localtime')),
    FOREIGN KEY (ticker) REFERENCES acoes(ticker)
);


ALTER TABLE acoes RENAME TO acoes_old;
CREATE TABLE IF NOT EXISTS acoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT,
    cotacao REAL,
    pl REAL,
    pvp REAL,
    dividend_yield REAL,
    payout REAL,
    date TEXT DEFAULT (date('now', 'localtime'))
);

INSERT INTO acoes (ticker, cotacao, pl, pvp, dividend_yield, payout, date)
SELECT ticker, cotacao, pl, pvp, dividend_yield, payout, date
FROM acoes_old;

DROP TABLE acoes_old;

COMMIT;
PRAGMA foreign_keys=on;