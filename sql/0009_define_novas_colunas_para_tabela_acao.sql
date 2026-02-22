-- sql/0009_define_novas_colunas_para_tabela_acao.sql
BEGIN TRANSACTION;

ALTER TABLE acao ADD COLUMN roa TEXT;
ALTER TABLE acao ADD COLUMN roic TEXT;
ALTER TABLE acao ADD COLUMN dl_patrimonio TEXT;
ALTER TABLE acao ADD COLUMN dl_ebitda TEXT;
ALTER TABLE acao ADD COLUMN dl_ebit TEXT;
ALTER TABLE acao ADD COLUMN db_patrimonio TEXT;
ALTER TABLE acao ADD COLUMN cagr_receitas_5_anos TEXT;
ALTER TABLE acao ADD COLUMN cagr_lucros_5_anos TEXT;
ALTER TABLE acao RENAME COLUMN dividend_yield TO dy;
COMMIT;
