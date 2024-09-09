from PySide6.QtCore import Qt, QTimer

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSizePolicy,
    QWidget,
    QMenu,
)

from paths import path_read_file
from models.ModelArt import ModelArt
from dataclasses import dataclass


@dataclass
class _ContractCell:
    column: int
    row: int
    value: str | None


class _ContextMenu(QMenu):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.event_update_action = None
        self.event_on_click_action = None
        self.event_call_context_menu = None
        self.addAction("Select all")
        self.addSeparator()
        self.addAction("Copy selected")
        self.addAction("Paste in selected")
        self.addAction("Delete selected")
        self.addSeparator()
        self._menu = self.addMenu('Scale')

        for size in ModelArt().resize.sizes:
            action = self._menu.addAction(f"Scale to {size}")
            action.setToolTip(size)

        parent.contextMenuEvent = self._context_menu_event

        # Triggered connect
        self._connect_triggered(self.actions())
        self._connect_triggered(self._menu.actions(), menu=self._menu)

    def _update_actions(self, actions: list[QAction], menu=None):
        for i, action in enumerate(actions):
            if len(action.text()):
                self.event_update_action(action, i, menu)

    def _connect_triggered(self, actions: list[QAction], menu=None):
        for i, action in enumerate(actions):
            if len(action.text()):
                action.triggered.connect(
                    lambda checked, arg1=action, arg2=i, arg3=menu: self._action_triggered(arg1, arg2, arg3)
                )

    def _action_triggered(self, action: QAction, action_id: int, menu: QAction.menu):
        if self.event_on_click_action is not None:
            self.event_on_click_action(action, action_id, menu)

    """ PySide events """
    def _context_menu_event(self, event):
        if self.event_call_context_menu is not None:
            self._update_actions(actions=self.actions())
            self._update_actions(actions=self._menu.actions(), menu=self._menu)
            self.exec(event.globalPos())


class ComponentArtBoard(QTableWidget):
    def __init__(self, parent: QWidget, rows: int, columns: int):
        super().__init__(rows, columns, parent)

        # MVC controller
        self._controller = None

        # QTableWidget / Header
        self.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # QTableWidget / Params
        self.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)
        self.setCornerButtonEnabled(False)

        # QTimer / sleep
        self._timer = QTimer()
        self._timer.setInterval(2000)

        # Create columns, rows
        for column in range(columns):
            for row in range(rows):
                item = QTableWidgetItem()
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                self.setItem(row, column, item)

        # Set css style
        self.setStyleSheet(path_read_file(file='art_board.css'))

        self.setContentsMargins(0, 0, 0, 0)

    def update_size(self, size: str):
        self._change_style(self.horizontalHeader(), name=size)
        self._change_style(self.verticalHeader(), name=size)

        for r in range(self.rowCount()):
            for c in range(self.columnCount()):
                self._change_style(self.item(r, c).tableWidget(), name=size)

        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    @staticmethod
    def _change_style(widget, name: str):
        widget_style = widget.style()
        widget.setObjectName(name)
        widget_style.unpolish(widget)
        widget_style.polish(widget)

    """ Methods """
    # bind MVC controller
    def bind_to_controller(self, controller):
        self.cellClicked.connect(controller.on_click_cell)
        context_menu = _ContextMenu(parent=self)
        context_menu.event_update_action = controller.update_action_in_context_menu
        context_menu.event_call_context_menu = controller.call_context_menu
        context_menu.event_on_click_action = controller.on_click_action

    def set_cell_text(self, column: int, row: int, cell_text: str):
        self.item(row, column).setText(cell_text)

    def set_cells_text(self, cells: list[_ContractCell, ...]):
        for cell in cells:
            if cell.value is not None:
                self.set_cell_text(column=cell.column, row=cell.row, cell_text=cell.value)

    def clear_cell_text(self, column: int, row: int):
        self.item(row, column).setText('')

    def clear_cells_text(self):
        for column in range(self.columnCount()):
            for row in range(self.rowCount()):
                item = self.item(row, column)
                if item.text():
                    item.setText('')

    def get_cell_text(self, column: int, row: int) -> str:
        return self.item(row, column).text()

    def get_cells_text(self) -> list[tuple[int, int, str]]:
        output: list[tuple[int, int, str]] = list()
        for column in range(self.columnCount()):
            for row in range(self.rowCount()):
                output.append((column, row, self.get_cell_text(column=column, row=row)))
        return output

    def items_count(self) -> int:
        return self.columnCount() + self.rowCount()

    def table_size(self) -> tuple[int, int]:
        return self.columnCount(), self.rowCount()
