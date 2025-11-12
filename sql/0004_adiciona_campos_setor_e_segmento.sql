-- sql/0004_adiciona_campos_setor_e_segmento.sql
PRAGMA foreign_keys=off;
BEGIN TRANSACTION;

ALTER TABLE acoes ADD COLUMN setor TEXT;
ALTER TABLE acoes ADD COLUMN segmento TEXT;

COMMIT;
PRAGMA foreign_keys=on;