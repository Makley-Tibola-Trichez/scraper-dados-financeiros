from enum import Enum

from gspread.cell import Cell


def make_cell(row: int, col_enum: Enum, value: str | None, force_update: bool = False) -> Cell | None:
    if force_update or value is not None:
        return Cell(row, col_enum.value, value)
    return None


def build_cells(row: int, values: list[tuple[Enum, str | None]], force_update: bool = False) -> list[Cell]:
    cells: list[Cell] = []
    for col_enum, value in values:
        cell = make_cell(row, col_enum, value, force_update)
        if cell is not None:
            cells.append(cell)
    return cells
