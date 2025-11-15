-- sql/0005_cria_tabela_dividendos_historico.sql

CREATE TABLE IF NOT EXISTS dividendos_historico (
    ticker TEXT,
    valor REAL,
    data_anuncio TIMESTAMP,
    data_pagamento TIMESTAMP,
    tipo TEXT,
    date TEXT DEFAULT CURRENT_DATE,

    PRIMARY KEY (ticker, valor, data_anuncio)
    FOREIGN KEY (ticker) REFERENCES acoes(ticker)
)
