from pydantic import BaseModel, Field


class Fii(BaseModel):
    ticker: str = Field(...)
    tipo_de_fundo: str = Field(...)
    segmento: str = Field(...)
    cotacao: str = Field(...)
    pvp: str = Field(...)
    quantidade_cotas_emitidas: str = Field(...)
    valor_patrimonial_por_cota: str = Field(...)
    dividendo_1_mes: str = Field(...)
    dividendo_3_meses: str = Field(...)
    dividendo_6_meses: str = Field(...)
    dividendo_12_meses: str = Field(...)
    dividend_yield_1_mes: str = Field(...)
    dividend_yield_3_meses: str = Field(...)
    dividend_yield_6_meses: str = Field(...)
    dividend_yield_12_meses: str = Field(...)
