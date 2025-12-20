from dataclasses import dataclass, field


@dataclass
class Config:
    id_worksheet_fiis_base: str = field(default="240919886")
    id_worksheet_acoes_teto_bazin: str = field(default="0")
