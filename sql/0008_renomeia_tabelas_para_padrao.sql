-- sql/0008_renomeia_tabelas_para_padrao.sql

BEGIN TRANSACTION;
ALTER TABLE dividendos_historico RENAME TO acao_historico_dividendos;
ALTER TABLE acoes RENAME TO acao;
ALTER TABLE fiis RENAME TO fii;
COMMIT;