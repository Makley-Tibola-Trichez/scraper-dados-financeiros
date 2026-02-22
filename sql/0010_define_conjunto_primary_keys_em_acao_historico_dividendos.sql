-- sql/0010_define_conjunto_primary_keys_em_acao_historico_dividendos.sql
BEGIN TRANSACTION;

CREATE UNIQUE INDEX IF NOT EXISTS idx_acao_historico_dividendos_ticker_valor_data_anuncio
ON acao_historico_dividendos (ticker, valor, data_anuncio);

COMMIT;
