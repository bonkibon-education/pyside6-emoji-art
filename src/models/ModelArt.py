import os
from typing import List

import emoji
from util import UtilMetaSingleton
from emoji import is_emoji


class _Cell:
    def __init__(self, column: int, row: int, value: str | None):
        self._column: int = column
        self._row: int = row
        self._value: str | None = value

    @property
    def row(self) -> int:
        return self._row

    @property
    def column(self) -> int:
        return self._column

    @property
    def value(self) -> str | None:
        return self._value

    @value.setter
    def value(self, string: str | None):
        if isinstance(string, str) or string is None:
            self._value = string
        else:
            raise ValueError(f'Invalid value: {string} (not type "str" or not type "None")')

    def is_empty(self) -> bool:
        return bool(self._value is None)


class _Table:
    def __init__(self, columns: int, rows: int):
        self._columns: int = columns
        self._rows: int = rows
        self._cells: list[list[_Cell]] = [
            [_Cell(column, row, value=None) for row in range(rows)] for column in range(columns)
        ]

    @property
    def columns(self) -> int:
        return self._columns

    @property
    def rows(self) -> int:
        return self._rows

    def get_cells(self, only_value: bool = False) -> list[list[str | None]] | list[list[_Cell]]:
        if only_value:
            return [
                [self._cells[column][row].value for row in range(self._rows)] for column in range(self._columns)
            ]

        return self._cells

    def cell(self, column: int, row: int) -> _Cell | None:
        self._validate_cell_index(column, row)
        return self._cells[column][row]

    def clear_cell(self, column: int, row: int):
        self._validate_cell_index(column, row)
        self._cells[column][row].value = None

    def clear_cells(self) -> None:
        for column in range(self._columns):
            for row in range(self._rows):
                self.clear_cell(column, row)

    def is_empty_cells(self) -> bool:
        for column in range(self._columns):
            for row in range(self._rows):
                if not self._cells[column][row].is_empty():
                    return False
        return True

    def change_cell(self, column: int, row: int, value: str | None) -> None:
        self._validate_cell_index(column, row)
        self._validate_cell_value(value)
        self._cells[column][row].value = value

    def change_cells(self, cells: list[_Cell]) -> None:
        for cell in cells:
            self.change_cell(column=cell.column, row=cell.row, value=cell.value)

    def cells_array1d(self) -> list[_Cell]:
        return [cell for cells in self._cells for cell in cells]

    def convert_to_text(self, replace_none: str = ''):
        text: str = ''
        for column in range(self._columns):
            for row in range(self._rows):
                value: str = self._cells[row][column].value
                text += replace_none if value is None else value
            text += '\n'
        return text

    def _validate_cell_index(self, column: int, row: int):
        if column >= self._columns or row >= self._rows:
            raise ValueError(f"Invalid cell index: ({column}, {row})")

    @staticmethod
    def _validate_cell_value(value: str | None):
        if not is_emoji(value) and value is not None:
            raise ValueError(f"Invalid cell value: {value} (not an emoji)")


class _ArtBoardResize:
    _size_id: int = 0
    _SIZES: tuple[str] = (
        '3x-large', '2x-large', 'x-large',
        'x-medium', 'medium',
        '2x-small', 'x-small', 'small',
    )

    @property
    def sizes(self):
        return self._SIZES

    @property
    def size(self) -> str:
        return self._SIZES[self._size_id]

    @property
    def size_id(self) -> int:
        return self._size_id

    @size.setter
    def size(self, value: str):
        self._validate_size_name(value)
        self._size_id = self._SIZES.index(value)

    @size_id.setter
    def size_id(self, value: int):
        self._validate_size_id(value)
        self._size_id = value

    @property
    def size_max(self) -> int:
        return len(self._SIZES)

    @property
    def size_middle(self) -> int:
        return (len(self._SIZES) - 1) // 2

    @property
    def size_name_min(self) -> str:
        return self._SIZES[0]

    @property
    def size_name_max(self) -> str:
        return self._SIZES[len(self._SIZES) - 1]

    @property
    def size_name_middle(self) -> str:
        return self._SIZES[(len(self._SIZES) - 1) // 2]

    def _validate_size_id(self, value: int):
        if 0 > value >= len(self._SIZES):
            raise ValueError(f'Invalid value: {value} (range of values {self._SIZES})')

    def _validate_size_name(self, value: str):
        if value not in self._SIZES:
            raise ValueError(f'Invalid value: {value} ({value} not in {self._SIZES})')


class _ArtBoard:
    def __init__(self):
        self._index: int = 0
        self._tables: list[_Table] = list()

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int):
        self._validate_table_index(value)
        self._index = value

    @property
    def arts(self) -> list[_Table]:
        return self._tables

    @property
    def art(self) -> _Table:
        return self._tables[self._index]

    def count(self) -> int:
        return len(self._tables)

    def add_art(self, column: int, row: int):
        self._validate_table_size(column, row)
        self._tables.append(_Table(columns=column, rows=row))

    def delete_art(self, index: int):
        self._validate_table_index(index)
        del self._tables[index]

    def insert_art(self, art, old_index, new_index: int):
        self._tables.pop(old_index)
        self._tables.insert(new_index, art)

    def _validate_table_index(self, index: int) -> None:
        if not (0 <= index < len(self._tables)):
            raise ValueError(f'Invalid value: {index} (range of values)')

    @staticmethod
    def _validate_table_size(column: int, row: int) -> None:
        if not isinstance(column, int) or not isinstance(row, int):
            raise ValueError(f'Invalid value: {column} or {row} (only int)')
        if column <= 0 or row <= 0:
            raise ValueError(f'Invalid value: {column} and {row} (>= 0)')


class ModelArt(metaclass=UtilMetaSingleton):
    def __init__(self):
        self._size_art_board: list[int, int] | tuple[int, int] | None = None
        self._filepath: str | None = None
        self._art_board = _ArtBoard()
        self._resize = _ArtBoardResize()

    @property
    def resize(self) -> _ArtBoardResize:
        return self._resize

    @property
    def art_board(self) -> _ArtBoard:
        return self._art_board

    @property
    def size_art(self) -> list[int, int] | tuple[int, int] | None:
        return self._size_art_board

    @size_art.setter
    def size_art(self, value: tuple[int, int]) -> None:
        self._validate_size(value)
        self._size_art_board = value

    @property
    def filepath(self) -> str | None:
        return self._filepath

    @filepath.setter
    def filepath(self, value: str):
        self._validate_filepath(value)
        self._filepath = value

    def is_valid_filepath(self) -> bool:
        if self._filepath is None:
            return False
        try:
            return True
        except (
            OSError,
            ValueError,
            FileExistsError,
            PermissionError,
            FileNotFoundError,
        ):
            return False

    @staticmethod
    def _validate_filepath(value: str) -> None:
        if not isinstance(value, str):
            raise ValueError(f'Invalid value type: {value} (not type "str")')
        if not os.path.isfile(value):
            raise FileNotFoundError(f"File: {value} not exists")
        if not value.endswith('.json'):
            raise ValueError("The file must have an extension .json")
        if not os.access(value, os.R_OK):
            raise PermissionError(f"Denied access to read the file {value}.")

    @staticmethod
    def _validate_size(value: tuple[int, int]) -> None:
        if not isinstance(value, tuple):
            raise ValueError(f'Invalid value: {value} (only tuple)')
        if len(value) != 2:
            raise ValueError(f'Invalid value: {value} (len != 2)')
