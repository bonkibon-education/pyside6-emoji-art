from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
)

from paths import path_read_file


class ComponentLabelNotification(QLabel):
    def __init__(self, parent: QWidget, text: str):
        super().__init__(parent)

        self.setText(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set css style
        self.setObjectName('label-notification')
        self.setStyleSheet(path_read_file(file='label_notification.css'))
        self.adjustSize()

    def set_hide(self, hide: bool):
        is_hidden: bool = self.isHidden()

        if is_hidden and hide or not is_hidden and not hide:
            return

        self.setHidden(hide)

    def move_to_center(self, size: QSize):
        hint_width, hint_height = self.sizeHint().width(), self.sizeHint().height()
        self.move((size.width() - hint_width) // 2, (size.height() - hint_height) // 2)
