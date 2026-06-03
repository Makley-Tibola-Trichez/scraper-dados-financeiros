-- sql/0012_redefine_unique_index_de_acao_historico_dividendos.sql

BEGIN TRANSACTION;

DROP INDEX IF EXISTS idx_acao_historico_dividendos_ticker_valor_data_anuncio;

CREATE UNIQUE INDEX idx_acao_historico_dividendos_ticker_valor_data_anuncio
ON acao_historico_dividendos (
    ticker,
    valor,
    data_anuncio,
    data_pagamento,
    tipo,
    criado_em
);


COMMIT;
