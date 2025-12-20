from dataclasses import dataclass


@dataclass
class FiiModel:
    id: int | None
    ticker: str
    tipo_de_fundo: str
    segmento: str
    cotacao: str
    pvp: str
    quantidade_cotas_emitidas: str
    valor_patrimonial_por_cota: str
    dividendo_1_mes: str
    dividendo_3_meses: str
    dividendo_6_meses: str
    dividendo_12_meses: str
    dividend_yield_1_mes: str
    dividend_yield_3_meses: str
    dividend_yield_6_meses: str
    dividend_yield_12_meses: str

    date: str
    # valor_patrimonial: int
    # gestora: str
    # administrador: str


class FiiTijoloModel(FiiModel):
    segmento: str
    numero_imoveis: int
    vacancia: str
    # vacancia_fisica: str
    # vacancia_financeira: str
    # wault: str
    # tipo_contrato: str
    # reajuste: str
    # qualidade_inquilino: str
    # concentracao_inquilino: str


class FiiPapelModel(FiiModel):
    # porcentagem_ipca: str
    # porcentagem_cdi: str
    # porcentagem_prefixado: str
    # porcentagem_indexado_total: str
    # spread_maximo: str
    # numero_cris: int
    concentracao_top_5: str
    porcentagem_caixa: str
    garantias: str
    risco_credito: str
