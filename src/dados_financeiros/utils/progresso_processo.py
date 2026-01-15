import os


class ProgressoProcessos:
    def __init__(self, total_processos: int, descricao_tipo_processo: str) -> None:
        self.total_processos = total_processos
        self.descricao_tipo_processo = descricao_tipo_processo

    def limpar_terminal(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def atualizar_progresso(self, nome_processo: str, indice_processo: int) -> None:
        self.limpar_terminal()
        progresso = (indice_processo / self.total_processos) * 100
        print("""============================""")
        print(f"Processo {self.descricao_tipo_processo}")
        print("""============================""")
        print(f"[{nome_processo}] Progresso: {progresso:.2f}% ({indice_processo}/{self.total_processos})")
