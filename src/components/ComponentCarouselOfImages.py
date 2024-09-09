from PySide6.QtCore import Qt, QSize, QMimeData
from PySide6.QtGui import QPixmap, QDrag
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QScrollArea,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
)

from paths import path_read_file
from util import util_convert_widget_to_pixmap
from components.ComponentLabelNotification import ComponentLabelNotification


class _ComponentCarouselItem(QWidget):
    def __init__(self, pixmap: QPixmap, title: str):
        super().__init__()

        self._drag = QDrag(self)
        self._mime_data = QMimeData()

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # QLabel | Image
        self._label = QLabel()
        self._label.setPixmap(pixmap)
        self._label.setScaledContents(True)
        self._label.setMaximumSize(QSize(100, 100))

        # QPushButton | Del button
        self._pushbutton = QPushButton(title)

        # QVBoxLayout | Main container
        self._vbox_layout = QVBoxLayout()
        self.setLayout(self._vbox_layout)
        self._vbox_layout.addWidget(self._label, alignment=Qt.AlignmentFlag.AlignCenter)
        self._vbox_layout.addWidget(self._pushbutton, alignment=Qt.AlignmentFlag.AlignCenter)

        # Widgets: change object name for css style
        self._label.setObjectName('label-carousel-item-image')
        self._pushbutton.setObjectName('button-carousel-item-delete')

    """ 
        TODO: 
            - add drag & drop;
    """
    """
    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            if e.buttons() == Qt.MouseButton.LeftButton:
                self._drag = QDrag(self)
                mime = QMimeData()
                self._drag.setMimeData(mime)
                self._drag.exec(Qt.DropAction.MoveAction)
    """

    # bind MVC controller
    def bind_to_controller(self, controller):
        self._label.mouseReleaseEvent = lambda event: controller.on_click_img_carousel_item(event, self)
        self._pushbutton.mouseReleaseEvent = lambda event: controller.on_click_del_carousel_item(event, self)

    def update_title(self, title: str):
        self._pushbutton.setText(title)


class ComponentCarouselOfImages(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.on_drop_and_insert_image = None

        # MVC controller
        self._controller = None

        # Widget params
        self.setAcceptDrops(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # QScrollArea
        self._scroll_area = QScrollArea(self)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
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
        self._notification = ComponentLabelNotification(parent=self, text='Carousel empty')
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
        self._scroll_area.setObjectName('scroll-area-carousel-of-images')
        self._widget.setObjectName('widget-carousel-of-images')

        # Set css style
        self.setStyleSheet(path_read_file(file='carousel_of_images.css'))

    """ Events """

    def resizeEvent(self, event):
        self._notification.move_to_center(event.size())

    """ 
        TODO: 
            - add drag & drop;
    """
    """
    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        # https://www.pythonguis.com/faq/pyside6-drag-drop-widgets/
        position = event.position()
        widget = event.source()
        counter: int = 0

        for counter in range(self._hbox_layout.count()):
            item = self._hbox_layout.itemAt(counter).widget()
            if position.x() < item.x() + item.size().width() // 2:
                break

        new_id: int = max(1, counter)
        self._hbox_layout.removeWidget(widget)
        self._hbox_layout.insertWidget(new_id, widget)
        event.accept()

        if self.on_drop_and_insert_image:
            self.on_drop_and_insert_image(event, new_id)
    """

    """ Methods """

    # bind MVC controller
    def bind_to_controller(self, controller):
        self._controller = controller

        """ 
            TODO: 
                - add drag & drop;
        """
        #self.on_drop_and_insert_image = self._controller.on_drop_and_insert_image

    def add_carousel_item(self, widget: QWidget) -> None:
        pixmap = util_convert_widget_to_pixmap(widget)
        item: _ComponentCarouselItem = _ComponentCarouselItem(
            pixmap=pixmap, title=f'del: [{self._hbox_layout.count()}]'
        )
        item.bind_to_controller(controller=self._controller)
        self._hbox_layout.addWidget(item, alignment=Qt.AlignmentFlag.AlignLeft)
        self._notification.set_hide(hide=True)

    def add_carousel_item_pixmap(self, pixmap: QPixmap) -> None:
        item = _ComponentCarouselItem(
            pixmap=pixmap, title=f'del: [{self._hbox_layout.count()}]'
        )
        item.bind_to_controller(controller=self._controller)
        self._hbox_layout.addWidget(item, alignment=Qt.AlignmentFlag.AlignLeft)
        self._notification.set_hide(hide=True)

    def del_carousel_item(self, index: int) -> None:
        widget: QWidget = self.item(index).widget()
        self._hbox_layout.removeWidget(widget)
        widget.deleteLater()
        del widget

        if self._hbox_layout.count() == 0:
            self._notification.set_hide(hide=False)

    def update_items_title(self):
        for i in range(self._hbox_layout.count()):
            item = self._hbox_layout.itemAt(i)
            if not item:
                continue
            if isinstance(item.widget(), _ComponentCarouselItem):
                item.widget().update_title(f'del: [{i}]')

    def item(self, index: int) -> QWidget:
        return self._hbox_layout.itemAt(index)

    def items(self) -> list[QWidget]:
        output: list[QWidget] = list()
        for i in range(self._hbox_layout.count()):
            item = self._hbox_layout.itemAt(i)
            output.append(item.widget())
        return output

    def items_count(self) -> int:
        return self._hbox_layout.count()

    def get_item_id(self, widget: QWidget) -> int:
        items: list[QWidget] = self.items()
        return items.index(widget)
