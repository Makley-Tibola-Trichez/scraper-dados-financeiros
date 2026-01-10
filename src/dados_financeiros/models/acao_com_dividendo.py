from models.acao import AcaoModel
from models.dividendo import DividendoAnualModel


class AcaoComDividendoModel(AcaoModel):
    dividendos_anuais: list[DividendoAnualModel]

    def set_dividendos_anuais(self, dividendos: list[DividendoAnualModel]) -> None:
        self.dividendos_anuais = dividendos

    def get_dividendos_anuais(self) -> list[DividendoAnualModel]:
        return self.dividendos_anuais
