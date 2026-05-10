-- sql/0011_define_nova_coluna_em_acao_historico_dividendos.sql

BEGIN TRANSACTION;

ALTER TABLE acao_historico_dividendos RENAME COLUMN 'date' to criado_em

COMMIT;