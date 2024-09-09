from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QScrollArea,
    QGridLayout,
    QSizePolicy,
    QFrame
)

from paths import path_read_file


class _Title(QLabel):
    def __init__(self, parent, title: str):
        super().__init__(title, parent)
        self.setObjectName('label-title-emoji-store')


class ComponentEmojiStore(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self._event = None

        # QScrollArea
        self._scroll_area = QScrollArea(self)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self._scroll_area.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self._scroll_area.setWidgetResizable(True)

        # QHBoxLayout
        self._widget = QWidget()
        self._grid_layout: QGridLayout = QGridLayout(self._widget)
        self._scroll_area.setWidget(self._widget)

        # QVBoxLayout
        self._vbox_layout = QVBoxLayout(self)
        self._vbox_layout.addWidget(self._scroll_area)
        self._vbox_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._vbox_layout)

        # Layouts indents
        self.setContentsMargins(0, 0, 0, 0)
        self._widget.setContentsMargins(0, 0, 0, 0)
        self._scroll_area.setContentsMargins(0, 0, 0, 0)
        self._grid_layout.setContentsMargins(0, 0, 0, 0)
        self._vbox_layout.setContentsMargins(0, 0, 0, 0)
        self._grid_layout.setSpacing(0)
        self._vbox_layout.setSpacing(0)

        # Widgets: change object name for css style
        self._widget.setObjectName('widget-emoji-store')
        self.setObjectName('frame-emoji-store')

        # Set css style
        self.setStyleSheet(path_read_file(file='emoji_store.css'))

    """ Event """
    def mousePressEvent(self, event):
        if self._event is not None:
            widget = self._grid_layout.itemAt(self._grid_layout.indexOf(self.childAt(event.pos())))
            if widget and not isinstance(self.childAt(event.pos()), _Title):
                self._event(event, widget.widget())

    """ Methods """
    # bind MVC controller
    def bind_to_controller(self, controller):
        self._event = controller.on_click_emoji_store

    def add_row(self, row: list[str]):
        row_count: int = self._grid_layout.rowCount()

        for column, text in enumerate(row):
            label = QLabel(text)
            label.setObjectName('label-row-emoji-store')
            self._grid_layout.addWidget(label, row_count, column, alignment=Qt.AlignmentFlag.AlignCenter)

    def add_title(self, title: str):
        widget_title = _Title(self, title)
        self._grid_layout.addWidget(widget_title, self._grid_layout.rowCount(), 0, 1, 0)
