from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class Dividendo(BaseModel):
    valor: float = Field(...)
    data_anuncio: datetime = Field(...)

    @field_validator("data_anuncio", mode="before")
    @classmethod
    def format_data_anuncio(cls, value: str | datetime) -> datetime:
        if isinstance(value, datetime):
            return value
        return datetime.fromisoformat(value).replace(tzinfo=None)

    data_pagamento: str | None = Field(...)
    tipo: str = Field(...)


class Acao(BaseModel):
    ticker: str = Field(..., min_length=1, max_length=10, description="Identificador da ação")
    cotacao: str = Field(..., title="Cotação")
    pl: str = Field(
        ...,
        title="P/L - Preço sobre o lucro",
    )
    pvp: str = Field(
        ...,
        title="P/PV - Preço sobre o valor patrimonial",
        description=" Abaixo de 1, indica que a empresa está sendo vendida por menos que seu valor real.",
    )
    lpa: str = Field(
        ...,
        title="L/P - Lucro por ação",
        description="Quando o número é negativo, indica que a empresa está operando com geração de prejuízo ao invés de lucro.",
    )
    dy: str = Field(..., title="DY - Dividend yield")
    roe: str = Field(
        ...,
        title="ROE - Retorno sobre o patrimônio líquido",
        description=r"Valores acima de 15% geralmente são considerados bons.",
    )
    roic: str = Field(
        ...,
        title="ROIC = Retorno sobre o Capital Investido",
        description=r"Mede o retorno sobre o capital investido em uma empresa. Quanto maior este indicador, melhor é o retorno que os investidores estão recebendo sobre o investimento. Valores acima de 10% geralmente são considerados bons.",
    )
    roa: str = Field(
        ...,
        title="ROA = Retorno sobre o Ativo",
        description=r"Mede a eficiência com que uma empresa utiliza seus ativos para gerar lucro. Quanto maior este indicador, melhor é a eficiência em gerar lucro a partir dos ativos. Valores acima de 10% geralmente são considerados bons.",
    )
    vpa: str = Field(..., title="VPA - Valor Patrimonial por Ação")
    payout: str = Field(..., title="PAYOUT - Quanto do lucro líquido foi distribuido aos acionanistas")
    setor: str = Field(..., title="Setor")
    segmento: str = Field(..., title="Segmento")

    dl_patrimonio: str = Field(
        ...,
        title="Dívida líquida sobre o patrimônio",
        description="Avalia a capacidade da empresa de cumprir suas obrigações financeiras. Quanto menor, menos endividada está a empresa. Valores abaixo de 1 indicam que a empresa possui mais patrimônio líquido do que dívida líquida.",
    )
    dl_ebitda: str = Field(
        ...,
        title="Dívida líquida sobre EBITDA",
        description="Mede a relação entre a dívida líquida de uma empresa e seu lucro antes de juros, impostos, depreciação e amortização (EBITDA). Quanto maior, maior é a carga de dívida da empresa.",
    )
    dl_ebit: str = Field(
        ...,
        title="Dívida líquida sobre EBIT",
        description="Mede a relação entre a dívida líquida de uma empresa e seu lucro antes de juros e impostos (EBIT). Esse indicador mostra o quanto a empresa está endividada em relação a sua capacidade de gerar lucro.",
    )
    db_patrimonio: str = Field(
        ...,
        title="Dívida bruta sobre valor de patrimônio",
        description="Indica o quanto a empresa está endividada em relação ao seu patrimônio. Quanto menor este número, melhor é a situação financeira da empresa.",
    )

    cagr_receitas_5_anos: str = Field(
        ...,
        title="CAGR Receitas 5 anos",
        description="CAGR = Compound Annual Growth Rate (crescimento anual composta).\nMede o crescimento da receita de uma empresa considerando os quatro últimos trimestres em comparação ao período de cinco anos atrás.",
    )

    cagr_lucros_5_anos: str = Field(
        ...,
        title="CAGR Lucros 5 anos",
        description="CAGR = Compound Annual Growth Rate (crescimento anual composta).\nMede o crescimento do lucro da empresa considerando os quatro últimos trimestres em comparação ao período equivalente de cinco anos atrás.",
    )

    dividendos: list[Dividendo] = Field(..., title="Dividendos declarados da ação")
