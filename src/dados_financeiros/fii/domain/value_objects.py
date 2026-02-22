from pydantic import BaseModel, Field


class Fii(BaseModel):
    ticker: str = Field(...)
    tipo_de_fundo: str = Field(...)
    segmento: str = Field(...)
    cotacao: str = Field(...)
    pvp: str = Field(...)
    quantidade_cotas_emitidas: str = Field(...)
    valor_patrimonial_por_cota: str = Field(...)
    div_1_mes: str = Field(...)
    div_3_meses: str = Field(...)
    div_6_meses: str = Field(...)
    div_12_meses: str = Field(...)
    dy_1_mes: str = Field(...)
    dy_3_meses: str = Field(...)
    dy_6_meses: str = Field(...)
    dy_12_meses: str = Field(...)
