from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QSizePolicy,
    QScrollArea,
    QVBoxLayout,
    QFrame
)


from paths import path_read_file
from components.ComponentLabelNotification import ComponentLabelNotification


class _Entry(QLabel):
    def __init__(self, parent, entry: str):
        super().__init__(entry, parent)
        self.setObjectName('label-entry-emoji-history')

    def bind_to_controller(self, controller):
        self.mousePressEvent = lambda event: controller.on_click_emoji_history(event, self)


class ComponentEmojiHistory(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self._controller = None
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # QScrollArea
        self._scroll_area = QScrollArea(self)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._scroll_area.setWidgetResizable(True)

        # QWidget
        self._widget = QWidget(self)
        self._widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        # QHBoxLayout
        self._hbox_layout: QHBoxLayout = QHBoxLayout(self._widget)
        self._scroll_area.setWidget(self._widget)

        # QVBoxLayout
        self._vbox_layout = QVBoxLayout(self)
        self._vbox_layout.addWidget(self._scroll_area)
        self._vbox_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self._vbox_layout)

        # ComponentLabelNotification
        self._notification = ComponentLabelNotification(parent=self, text='History empty')
        self._notification.show()

        # Layouts indents
        self.setContentsMargins(0, 0, 0, 0)
        self._widget.setContentsMargins(0, 0, 0, 0)
        self._scroll_area.setContentsMargins(0, 0, 0, 0)
        self._hbox_layout.setContentsMargins(0, 0, 0, 0)
        self._vbox_layout.setContentsMargins(0, 0, 0, 0)
        self._hbox_layout.setSpacing(0)
        self._vbox_layout.setSpacing(0)

        # Widgets: change object name for css style
        self._widget.setObjectName('widget-emoji-history')
        self.setObjectName('frame-emoji-history')

        # Set css style
        self.setStyleSheet(path_read_file(file='emoji_history.css'))

    # bind MVC controller
    def bind_to_controller(self, controller):
        self._controller = controller

    def add_entry(self, entry: str):
        self._hbox_layout.addWidget(self._new_entry(entry), alignment=Qt.AlignmentFlag.AlignCenter)
        self._notification.set_hide(hide=True)

    def insert_entry(self, entry: str):
        self._hbox_layout.insertWidget(0, self._new_entry(entry), alignment=Qt.AlignmentFlag.AlignCenter)
        self._notification.set_hide(hide=True)

    def del_entry(self, index: int):
        item = self._hbox_layout.itemAt(index)
        if item is not None:
            item.widget().deleteLater()
            self._hbox_layout.removeWidget(item.widget())
            if self._hbox_layout.count() == 0:
                self._notification.set_hide(hide=False)
            del item

    def _new_entry(self, entry: str):
        widget_entry = _Entry(parent=self, entry=entry)
        widget_entry.bind_to_controller(controller=self._controller)
        return widget_entry

    def items(self) -> list[str]:
        output: list[str] = list()
        for i in range(self._hbox_layout.count()):
            output.append(self._hbox_layout.itemAt(i).widget().text())
        return output

    def resizeEvent(self, event):
        self._notification.move_to_center(event.size())
