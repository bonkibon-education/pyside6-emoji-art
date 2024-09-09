from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
    QVBoxLayout,
    QFrame,
)

from settings import SETTINGS_SHORTCUTS
from paths import path_read_file


class _Shortcut(QPushButton):
    def __init__(self, parent, name: str, tool_tip: str):
        super().__init__(name, parent)

        self.setToolTip(tool_tip)
        self.setObjectName('pushbutton-shortcut')
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def bind_to_controller(self, controller):
        self.clicked.connect(lambda event: controller.on_click_shortcuts_item(event, self))


class ComponentShortcuts(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self._event = None

        # QHBoxLayout
        self._hbox_layout = QHBoxLayout(self)
        self.setLayout(self._hbox_layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Shortcut
        for shortcut in SETTINGS_SHORTCUTS.items():
            pushbutton = _Shortcut(
                parent=self,
                name=shortcut[1]['shortcut'],
                tool_tip=shortcut[0]
            )
            self._hbox_layout.addWidget(pushbutton)

        # Layout indents
        self._hbox_layout.setSpacing(24)
        self.setContentsMargins(0, 0, 0, 0)
        self._hbox_layout.setContentsMargins(0, 0, 0, 0)

        # Widgets: change object name for css style
        self.setObjectName('frame-shortcuts')

        # Set css style
        self.setStyleSheet(path_read_file(file='shortcuts.css'))

    # bind MVC controller
    def bind_to_controller(self, controller):
        for i in range(self._hbox_layout.count()):
            widget = self._hbox_layout.itemAt(i)
            if widget:
                _shortcut: _Shortcut | QWidget = widget.widget()
                _shortcut.bind_to_controller(controller=controller)
