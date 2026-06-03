-- sql/0013_nova_abordagem_para_acao_historico_dividendos.sql

CREATE TABLE IF NOT EXISTS novo_acao_historico_dividendos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT,
    valor REAL,
    data_anuncio TIMESTAMP,
    data_pagamento TIMESTAMP,
    tipo TEXT,
    criado_em TEXT DEFAULT CURRENT_DATE,

    FOREIGN KEY (ticker) REFERENCES acoes(ticker)
);


DROP TABLE acao_historico_dividendos;


ALTER TABLE novo_acao_historico_dividendos RENAME TO acao_historico_dividendos;

