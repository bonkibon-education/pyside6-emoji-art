from PySide6.QtCore import Qt, QRect, QPoint, QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QFrame,
    QSizePolicy,
    QMessageBox,
    QSizeGrip,
    QTableWidget,
)

from util import util_send_messagebox
from plugins.api_emoji_store import api_emoji_store
from components.ComponentArtBoard import ComponentArtBoard
from components.ComponentShortcuts import ComponentShortcuts
from components.ComponentEmojiStore import ComponentEmojiStore
from components.ComponentEmojiHistory import ComponentEmojiHistory
from components.ComponentCarouselOfImages import ComponentCarouselOfImages
from components.ComponentToastMessage import ComponentToastMessage, ExceptionToastMessageLimit


class _TopPanel(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        # Components
        self.component_art_board: ComponentArtBoard | None = None
        self.component_emoji_store: ComponentEmojiStore | None = None
        self.component_emoji_history: ComponentEmojiHistory | None = None

        # QHBoxLayout
        self._hbox_layout = QHBoxLayout()
        self.setLayout(self._hbox_layout)

        # QHBoxLayout
        self._vbox_layout = QVBoxLayout()

        # Layout indents
        self._vbox_layout.setSpacing(0)
        self._hbox_layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self._vbox_layout.setContentsMargins(0, 0, 0, 0)
        self._hbox_layout.setContentsMargins(0, 0, 0, 0)

    def bind_to_controller(self, controller):
        self.component_art_board.bind_to_controller(controller)
        self.component_emoji_store.bind_to_controller(controller)
        self.component_emoji_history.bind_to_controller(controller)

    def add_main_art_board(self, size: list[int, int] | tuple[int, int]):
        self.component_art_board: QTableWidget = ComponentArtBoard(self, columns=size[0], rows=size[1])
        self._hbox_layout.addWidget(self.component_art_board)

    def add_emoji_history(self):
        label = QLabel('History')
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setObjectName('label-title-panel')
        self.component_emoji_history = ComponentEmojiHistory(self)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(label)
        vbox_layout.addWidget(self.component_emoji_history)
        self._hbox_layout.addLayout(self._vbox_layout)
        self._vbox_layout.addLayout(vbox_layout)

        # Layout indents
        self._vbox_layout.setSpacing(0)
        self._vbox_layout.setContentsMargins(0, 0, 0, 0)

    def add_emoji_store(self):
        label = QLabel('Store')
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setObjectName('label-title-panel')
        self.component_emoji_store = ComponentEmojiStore(self)

        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(label)
        vbox_layout.addWidget(self.component_emoji_store)
        self._hbox_layout.addLayout(self._vbox_layout)
        self._vbox_layout.addLayout(vbox_layout)

        # Layout indents
        self._vbox_layout.setSpacing(0)
        self._vbox_layout.setContentsMargins(0, 0, 0, 0)

        # Fill emoji store
        json_data: dict = api_emoji_store.read_json_file()
        rows: list = list()

        def add_row(row: list[str]):
            self.component_emoji_store.add_row(row=row)

        def add_title(category: str):
            self.component_emoji_store.add_title(category)

        for category, value in json_data.items():
            add_title(category=category)
            for subcategories, emojis in value.items():
                for emoji in emojis:
                    if len(rows) < 6:
                        rows.append(emoji['character'])
                        continue

                    add_row(row=rows)
                    rows.clear()
                    continue


class _BottomPanel(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        # Components
        self.component_shortcuts: ComponentShortcuts | None = None
        self.component_carousel_of_images: ComponentCarouselOfImages | None = None

        # QHBoxLayout
        self._vbox_layout = QVBoxLayout()
        self.setLayout(self._vbox_layout)

        # Layout indents
        self._vbox_layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self._vbox_layout.setContentsMargins(0, 0, 0, 0)

    def bind_to_controller(self, controller):
        self.component_carousel_of_images.bind_to_controller(controller)
        self.component_shortcuts.bind_to_controller(controller)

    def add_carousel_of_images(self):
        self.component_carousel_of_images = ComponentCarouselOfImages(self)
        self._vbox_layout.addWidget(self.component_carousel_of_images)

    def add_shortcuts(self):
        self.component_shortcuts = ComponentShortcuts(self)
        self._vbox_layout.addWidget(self.component_shortcuts)


class ViewWorkspace(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set fixed height / block resize height
        self.setMaximumSize(self.maximumWidth(), 0)

        # MVC controller
        self._controller = None

        # Current toast pos / Window size
        self._toast_pos: tuple[int, int] = self.sizeHint().toTuple()

        # QWidget
        self._widget = QWidget()
        self.setCentralWidget(self._widget)

        # QHBoxLayout
        self._layout = QVBoxLayout()
        self._widget.setLayout(self._layout)

        # Top panel
        self._top_panel = _TopPanel(parent=self)
        self._top_panel.add_main_art_board(size=(10, 10))
        self._top_panel.add_emoji_store()
        self._top_panel.add_emoji_history()
        self._top_panel.component_emoji_history.setFixedWidth(self._top_panel.component_emoji_store.sizeHint().width())

        # Bottom panel
        self._bottom_panel = _BottomPanel(parent=self)
        self._bottom_panel.add_carousel_of_images()
        self._bottom_panel.add_shortcuts()
        self._bottom_panel.component_carousel_of_images.setFixedHeight(180)

        # Add widgets to layout
        self._layout.addWidget(self._top_panel, alignment=Qt.AlignmentFlag.AlignTop)
        self._layout.addWidget(self._bottom_panel, alignment=Qt.AlignmentFlag.AlignTop)

        # Layout indents
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

    @property
    def component_art_board(self):
        return self._top_panel.component_art_board

    @property
    def component_emoji_history(self):
        return self._top_panel.component_emoji_history

    @property
    def component_emoji_store(self):
        return self._top_panel.component_emoji_store

    @property
    def component_carousel_of_images(self):
        return self._bottom_panel.component_carousel_of_images

    @property
    def component_shortcuts(self):
        return self._bottom_panel.component_shortcuts

    def bind_to_controller(self, controller):
        self._top_panel.bind_to_controller(controller)
        self._bottom_panel.bind_to_controller(controller)

    def show_toast_message(self, title: str, message: str, duration: int):
        try:
            ComponentToastMessage(self, title, message, duration, (self._toast_pos[0], self._toast_pos[1])).show()
        except ExceptionToastMessageLimit as error:
            self.show_messagebox(title, str(error), status='error')

    @staticmethod
    def show_messagebox(title: str, message: str, status: str):
        util_send_messagebox(title=title, text=message, icon_status=status)

    def resizeEvent(self, event):
        self._toast_pos = event.size().toTuple()
