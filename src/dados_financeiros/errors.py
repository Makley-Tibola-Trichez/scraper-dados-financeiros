class ElementoNaoEncontradoError(Exception):
    """Erro lançado quando o Selenium não encontra o elemento desejado."""

    def __init__(self, mensagem: str = "Elemento não encontrado na página.", seletor: str | None = None) -> None:
        self.mensagem = mensagem
        self.seletor = seletor
        if seletor:
            self.mensagem += f" Seletor usado: {seletor}"
        super().__init__(self.mensagem)
