from gspread.cell import Cell


class Cells:
    row: int
    def __init__(self, row: int):
        self.row = row
    
    def cell_cotacao(self, value: str | None, force_update: bool = False) -> Cell | None:
        if force_update or value is not None:
            return Cell(self.row, 4, value)
        return None
    
    def cell_pl(self, value: str | None, force_update: bool = False) -> Cell | None:
        if force_update or value is not None:
            return Cell(self.row, 5, value)
        return None
    def cell_pvp(self, value: str | None, force_update: bool = False) -> Cell | None:
        if force_update or value is not None:
            return Cell(self.row, 6, value)
        return None
    def cell_dividend_yield(self, value: str | None, force_update: bool = False) -> Cell | None:
        if force_update or value is not None:
            return Cell(self.row, 7, value)
        return None
    def cell_payout(self, value: str | None, force_update: bool = False) -> Cell | None:
        if force_update or value is not None:
            return Cell(self.row, 8, value)
        return None
    def cells_dividendos(self, values: list[str], force_update: bool = False) -> list[Cell]:
        cells: list[Cell] = []
        start_col = 11
        for i, value in enumerate(values):
            if force_update or value is not None:
                cells.append(Cell(self.row, start_col + i, value))
        return cells
    
        