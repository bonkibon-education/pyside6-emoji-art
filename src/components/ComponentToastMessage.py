from PySide6.QtCore import Qt, QTimer, QRect, QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFrame,
    QSizePolicy,
    QProgressBar,
)

from paths import path_read_file


class ExceptionToastMessageLimit(Exception):
    pass


class _ProgressBar(QProgressBar):
    def __init__(self, parent, value: int, minimum: int, maximum: int):
        super().__init__(parent)

        # QProgressBar settings
        self.setValue(value)
        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.setMaximumHeight(6)
        self.setTextVisible(False)

        # Layouts indents
        self.setContentsMargins(0, 0, 0, 0)

        # Widgets: change object name for css style
        self.setObjectName('progressbar-tm')

    def update_progress(self, update_time: int):
        self.setValue(self.value() + update_time)


class _FrameTopBar(QFrame):
    def __init__(self, parent, title: str):
        super().__init__(parent)

        # QHBoxLayout
        self._hbox_layout = QHBoxLayout(self)
        self.setLayout(self._hbox_layout)

        # QLabel
        self._label = QLabel(title, self)
        self._label.setWordWrap(True)

        # QPushButton
        self.pushbutton = QPushButton('X', self)

        # Add widgets in layout
        self._hbox_layout.addWidget(self._label, alignment=Qt.AlignmentFlag.AlignLeft)
        self._hbox_layout.addWidget(self.pushbutton, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        # Layouts indents
        self._hbox_layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self._hbox_layout.setContentsMargins(0, 0, 0, 0)

        # Widgets: change object name for css style
        self.setObjectName('frame-tm-top-bar')
        self._label.setObjectName('label-tm-top-bar')
        self.pushbutton.setObjectName('pushbutton-tm-top-bar')


class _FrameBody(QFrame):
    def __init__(self, parent, message: str):
        super().__init__(parent)

        # QVBoxLayout
        self._vbox_layout = QVBoxLayout(self)
        self.setLayout(self._vbox_layout)

        # QLabel / Body
        self._label = QLabel(message, self)
        self._label.setWordWrap(True)
        self._vbox_layout.addWidget(self._label, alignment=Qt.AlignmentFlag.AlignTop)

        # Layouts indents
        self._vbox_layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self._vbox_layout.setContentsMargins(0, 0, 0, 0)

        # Widgets: change object name for css style
        self.setObjectName('frame-tm-body')
        self._label.setObjectName('label-tm-body')


class ComponentToastMessage(QFrame):
    __object_counter: int = 0

    @classmethod
    def add_count(cls):
        cls.__object_counter += 1

    @classmethod
    def sub_count(cls):
        cls.__object_counter -= 1

    @classmethod
    def obj_counter(cls):
        return cls.__object_counter

    def __new__(cls, *args, **kwargs):
        if cls.obj_counter() >= 3:
            raise ExceptionToastMessageLimit(f"Cannot create more than 3 instances of the {cls.__name__} class.")
        cls.add_count()
        return super(ComponentToastMessage, cls).__new__(cls)

    def __init__(self, parent: QWidget, title: str, message: str, duration: int, start_pos: tuple[int, int]):
        super().__init__(parent)

        self._start_pos = start_pos
        self._duration = duration

        # Set css style
        self.setStyleSheet(path_read_file(file='toast_message.css'))

        # SizePolicy
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Variables
        _timer_step = round(duration * 0.01)

        # QVBoxLayout
        self._vbox_layout = QVBoxLayout(self)
        self.setLayout(self._vbox_layout)

        # Widgets
        self._top_bar = _FrameTopBar(self, title=title)
        self._body = _FrameBody(self, message=message)
        self._progress_bar = _ProgressBar(self, value=0, minimum=0, maximum=duration)
        self._progress_bar.update_progress(_timer_step)

        # Qtimer
        self._timer = QTimer(self)
        self._timer.setInterval(_timer_step)
        self._timer.timeout.connect(lambda: self._event_update_timer(_timer_step, duration))
        self._timer.start()

        # Add widgets to layout
        self._vbox_layout.addWidget(self._top_bar)
        self._vbox_layout.addWidget(self._body)
        self._vbox_layout.addWidget(self._progress_bar)

        # Layouts indents
        self.adjustSize()
        self._vbox_layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self._vbox_layout.setContentsMargins(0, 0, 0, 0)

        # Widgets: change object name for css style
        self.setObjectName('frame-tm-item')

        # Events
        self._top_bar.pushbutton.clicked.connect(self._delete_item)

    """ Events """
    def mousePressEvent(self, event):
        self._delete_item()

    def enterEvent(self, event):
        self._timer.stop()

    def leaveEvent(self, event):
        self._timer.start()

    def _event_update_timer(self, timer_step: int, duration: int):
        if self._progress_bar.value() >= duration:
            self._delete_item()
            return
        self._progress_bar.update_progress(timer_step)

    """ Methods """
    def _add_animation(self, pos: tuple, duration: int):
        # Self size
        anim_w, anim_h = self.sizeHint().toTuple()

        # Counter
        obj_counter: int = self.obj_counter()

        # Animation pos
        padding_top: int = 8
        start_pos: tuple = (pos[0], pos[1])
        end_pos: tuple = (
            start_pos[0],
            start_pos[1] - (anim_h * obj_counter) - padding_top * obj_counter
        )

        # Animation start
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(min(800, duration))
        self._animation.setStartValue(QRect(*start_pos, anim_w, anim_h))
        self._animation.setEndValue(QRect(*end_pos, anim_w, anim_h))
        self._animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self._animation.start()

    def _delete_item(self):
        self._timer.stop()
        self.deleteLater()
        self.sub_count()
        del self

    def resizeEvent(self, event):
        # FrameSize
        size = self.frameSize()

        # Move
        self._add_animation(pos=(
            self._start_pos[0] - size.width(),
            self._start_pos[1]
            ), duration=self._duration
        )
