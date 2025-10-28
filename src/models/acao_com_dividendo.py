
from models.acao import AcaoModel
from models.dividendo import DividendoModel


class AcaoComDividendoModel(AcaoModel):
    dividendos_anuais: list[DividendoModel]
    
    def set_dividendos_anuais(self, dividendos: list[DividendoModel]) -> None:
        self.dividendos_anuais = dividendos
        
    def get_dividendos_anuais(self) -> list[DividendoModel]:
        return self.dividendos_anuais
    
    
    
    