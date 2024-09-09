from PIL import Image, ImageDraw, ImageFont
from dataclasses import dataclass


@dataclass
class _ContractCell:
    column: int
    row: int
    value: str | None


class _Cell(_ContractCell):
    def __init__(self, column: int, row: int, value: str | None, font_size: int, padding: int):
        super().__init__(column, row, value)
        self._width = font_size + padding
        self._height = font_size + padding
        self._padding: int = padding

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def x(self) -> int:
        return self._width - self._padding + (self._width * self.column)

    @property
    def y(self) -> int:
        return self._height - self._padding + (self._height * self.row)


class ApiDrawTable:
    def __init__(self, font: tuple[str, int], bg: str):
        self._background_color = bg
        self._image_font: ImageFont = ImageFont.truetype(font[0], font[1])

    def draw_table(self, cells: list[_ContractCell]) -> Image:
        table_cells: tuple[_Cell, ...] = self._table_data(cells)
        image_size: tuple[int, int] = self._calculate_img_size(table_cells)
        image = Image.new("RGB", image_size, self._background_color)
        draw = ImageDraw.Draw(image)

        for cell in table_cells:
            draw.text(
                xy=(cell.x, cell.y),
                text='' if cell.value is None else cell.value,
                embedded_color=True,
                font=self._image_font,
                anchor='mm'
            )

        return image

    @staticmethod
    def _calculate_img_size(table_cells) -> tuple[int, int]:
        cell: _Cell = table_cells[-1]
        return cell.x + cell.width, cell.y + cell.height

    def _table_data(self, cells: list[_ContractCell]) -> tuple[_Cell, ...]:
        return tuple(
            _Cell(
                row=cell.row,
                column=cell.column,
                font_size=int(self._image_font.size),
                padding=int(self._image_font.size) // 2,
                value=cell.value
            )
            for cell in cells
        )
