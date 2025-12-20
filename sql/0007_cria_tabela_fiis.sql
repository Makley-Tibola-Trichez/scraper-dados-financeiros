-- sql/0007_cria_tabela_fiis.sql
CREATE TABLE IF NOT EXISTS fiis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT,
    tipo_de_fundo TEXT,
    segmento TEXT,
    cotacao REAL,
    pvp REAL,
    quantidade_cotas_emitidas REAL,
    valor_patrimonial_por_cota REAL,
    dividend_yield_1_mes REAL,
    dividend_yield_3_meses REAL,
    dividend_yield_6_meses REAL,
    dividend_yield_12_meses REAL,
    dividendo_1_mes REAL,
    dividendo_3_meses REAL,
    dividendo_6_meses REAL,
    dividendo_12_meses REAL,

    date TEXT DEFAULT CURRENT_DATE
)
