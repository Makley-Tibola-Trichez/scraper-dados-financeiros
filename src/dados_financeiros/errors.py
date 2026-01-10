class ElementoNaoEncontradoError(Exception):
    """Erro lançado quando o Selenium não encontra o elemento desejado."""

    def __init__(self, mensagem: str = "Elemento não encontrado na página.", seletor: str | None = None) -> None:
        self.mensagem = mensagem
        self.seletor = seletor
        if seletor:
            self.mensagem += f" Seletor usado: {seletor}"
        super().__init__(self.mensagem)


class SemHistoricoDeDividendosError(Exception):
    """Erro lançado quando ao acessar a página de histórico de dividendos do fundamentus, e não encontra a tabela"""

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker
        mensagem = f"[{ticker}] - Não foi encontrado histórico de dividendos"
        self.mensagem = mensagem
        super().__init__(mensagem)
