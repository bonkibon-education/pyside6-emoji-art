from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap, QFont, QPainter
from PySide6.QtWidgets import QWidget, QMessageBox
from settings import SETTINGS_MESSAGEBOX_ICON


class UtilMetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(UtilMetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def util_switch_to_view(current_view: QWidget, new_view: QWidget) -> bool:
    if current_view is None or new_view is None:
        return False

    current_view.close()
    new_view.show()
    return True


def util_send_messagebox(title: str, text: str, icon_status: str):
    msgbox = QMessageBox()
    msgbox.setWindowTitle(title)
    msgbox.setIcon(SETTINGS_MESSAGEBOX_ICON.get(icon_status[0]))
    msgbox.setText(text)
    msgbox.exec()


def util_convert_widget_to_pixmap(widget: QWidget) -> QPixmap:
    size: QSize = QSize(widget.width(), widget.height())
    pixmap: QPixmap = QPixmap(size)
    widget.render(pixmap)
    return pixmap


def util_convert_text_to_pixmap(text: str) -> QPixmap:
    # QFont
    font = QFont()
    font.setPointSize(10)
    font.setFamily('Consolas')

    # QPixmap
    pixmap = QPixmap(16, 16)
    pixmap.fill(Qt.transparent)

    # QPainter
    painter = QPainter(pixmap)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, text)
    painter.end()

    return pixmap
