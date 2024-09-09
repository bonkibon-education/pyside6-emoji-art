from emoji import is_emoji

from PySide6.QtCore import Qt

from PySide6.QtGui import (
    QGuiApplication,
    QShortcut,
    QKeySequence,
    QPixmap,
    QImage
)

from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QMessageBox,
    QFileDialog
)

from models.ModelArt import ModelArt
from models.ModelEmojiHistory import (
    ModelEmojiHistory,
    DuplicateEntryError,
    LimitEntryError
)

from views.ViewWorkspace import ViewWorkspace
from controllers.DefaultController import DefaultController
from settings import SETTINGS_SHORTCUTS, SETTINGS_SHORTCUTS_HTML

from plugins.api_draw_table.api_draw_table import ApiDrawTable
from plugins.api_export_frames.api_export_frames import api_export_frames


class _ControllerArtBoard:
    def __init__(self, view: ViewWorkspace, model: ModelArt, clipboard):
        self.view = view
        self.model = model
        self.clipboard = clipboard
        self.component_art_board = self.view.component_art_board

    def on_press_shortcut_clear_current_art_board(self):
        if self.model.art_board.art.is_empty_cells():
            self.view.show_toast_message(
                title='Error',
                message='All cells of the art board are empty',
                duration=2000
            )
            return

        reply: QMessageBox.StandardButton = QMessageBox.question(
            self.view,
            "Confirm action",
            f"{SETTINGS_SHORTCUTS['ClearCurrentArtBoard']['description']}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.component_art_board.clear_cells_text()
            self.model.art_board.art.clear_cells()

    """ 
        Art board
    """
    def call_context_menu(self, actions: list):
        pass

    def update_action_in_context_menu(self, action, action_id: int, menu):
        if menu is not None:
            action.setDisabled(self.model.resize.size == action.toolTip())
            return

        match action_id:
            case 0:
                flag: bool = bool(
                    self.component_art_board.columnCount() * self.component_art_board.rowCount()
                    == len(self.component_art_board.selectedItems())
                )
                action.setDisabled(flag)
            case 1:
                pass
            case 2 | 4:
                selected = self.component_art_board.selectedItems()

                for item in selected:
                    if item.text():
                        action.setDisabled(False)
                        return

                action.setDisabled(True)
            case 3:
                clipboard_text: str = self.clipboard.text()

                if not is_emoji(clipboard_text):
                    action.setDisabled(True)
                    return

                selected = self.component_art_board.selectedItems()

                if not len(selected):
                    action.setDisabled(True)
                    return

                action.setDisabled(False)

    def on_click_action(self, action, action_id, menu):
        if menu is not None and menu.title() == 'Scale':
            self.model.resize.size = action.toolTip()
            self.component_art_board.update_size(size=self.model.resize.size)
            return

        match action_id:
            case 0:
                self.component_art_board.selectAll()
            case 1:
                pass
            case 2:
                self.clipboard.setText(''.join([
                    self.component_art_board.itemFromIndex(index).text()
                    for index in self.component_art_board.selectedIndexes()
                ]))
                self.component_art_board.clearSelection()
            case 3:
                text: str = self.clipboard.text()
                selected_indexes = self.component_art_board.selectedIndexes()
                for index in selected_indexes:
                    self.component_art_board.itemFromIndex(index).setText(text)
                    self.model.art_board.art.change_cell(column=index.column(), row=index.row(), value=text)
                self.component_art_board.clearSelection()
            case 4:
                selected_indexes = self.component_art_board.selectedIndexes()
                for index in selected_indexes:
                    self.component_art_board.itemFromIndex(index).setText('')
                    self.model.art_board.art.clear_cell(column=index.column(), row=index.row())
                self.component_art_board.clearSelection()

    def on_click_cell(self, row: int, column: int):
        clipboard_text: str = self.clipboard.text()
        self.component_art_board.clearSelection()

        if not is_emoji(clipboard_text):
            self.view.show_toast_message(
                title='Error',
                message='A cell can only contain the emoji value',
                duration=2000
            )
        elif not self.component_art_board.get_cell_text(column, row):
            self.component_art_board.set_cell_text(column, row, clipboard_text)
            self.model.art_board.art.change_cell(column, row, clipboard_text)
        else:
            self.component_art_board.clear_cell_text(column, row)
            self.model.art_board.art.clear_cell(column, row)


class _ControllerEmojiStore:
    def __init__(self, view: ViewWorkspace, model2: ModelEmojiHistory, clipboard):
        self.view = view
        self.model2 = model2
        self.clipboard = clipboard
        self.component_emoji_history = self.view.component_emoji_history

    def on_click_emoji_store(self, event, widget: QLabel):
        text: str = widget.text()
        self.clipboard.setText(text)

        try:
            self.model2.insert_entry(text)
            self.component_emoji_history.insert_entry(text)
            return
        except LimitEntryError:
            # Remove last item
            index: int = self.model2.get_last_entry()[1]
            self.model2.del_entry(index=index)
            self.component_emoji_history.del_entry(index=index)

            # Add new item
            self.model2.insert_entry(text)
            self.component_emoji_history.insert_entry(text)
            return
        except DuplicateEntryError:
            return


class _ControllerEmojiHistory:
    def __init__(self, view: ViewWorkspace, model2: ModelEmojiHistory, clipboard):
        self.view = view
        self.model2 = model2
        self.clipboard = clipboard

    def on_click_emoji_history(self, event, widget: QLabel):
        try:
            self.clipboard.setText(widget.text())
        except Exception as error:
            self.view.show_toast_message(title='Error', message=str(error), duration=4000)


class _ControllerCarouselOfImages:
    """
        TODO:
            def on_drop_and_insert_image(self, event, insert_id: int):
                pass
    """
    def __init__(self, view: ViewWorkspace, model: ModelArt):
        self.view = view
        self.model = model
        self.component_art_board = self.view.component_art_board
        self.component_carousel_of_images = self.view.component_carousel_of_images
        self.api_draw_table = ApiDrawTable(font=('seguiemj.ttf', 24), bg='black')

    def on_press_shortcut_add_carousel_item(self):
        # Clear current art board
        self.component_art_board.clear_cells_text()

        # Add carousel item
        image = self.api_draw_table.draw_table(cells=self.model.art_board.art.cells_array1d())
        self.component_carousel_of_images.add_carousel_item_pixmap(self._pillow_image_to_pixmap(image))
        self.component_carousel_of_images.update_items_title()

        # Create new model-art_board
        self.model.art_board.add_art(*self.component_art_board.table_size())
        self.model.art_board.index = self.model.art_board.count() - 1

    @staticmethod
    def _pillow_image_to_pixmap(image) -> QPixmap:
        image_data = image.tobytes("raw", "RGB")
        image_size = image.size
        return QPixmap.fromImage(
            QImage(
                image_data, image_size[0], image_size[1], QImage.Format.Format_RGB888
            )
        )

    def on_click_del_carousel_item(self, event, item):
        # Get carousel item id on click
        item_id: int = self.component_carousel_of_images.get_item_id(item)

        # Delete carousel item
        self.component_carousel_of_images.del_carousel_item(item_id)
        self.component_carousel_of_images.update_items_title()

        # Delete model-art_board
        self.model.art_board.delete_art(item_id)
        self.model.art_board.index = self.model.art_board.count() - 1

    def on_click_img_carousel_item(self, event, item):
        """
            TODO:
                - add inserting widgets (drag & drop);
                - add edit mode for current art on click
                - add menu (1 - copy art; 2 - delete art; 3 - edit art)
        """

        # Get carousel item id on click
        item_id: int = self.component_carousel_of_images.get_item_id(item)

        if event.button() == Qt.MouseButton.RightButton:
            self._copy_image_carousel_item(item_id)
            return

        # Delete carousel item
        self.component_carousel_of_images.del_carousel_item(item_id)
        self.component_carousel_of_images.update_items_title()

        # Delete model-art_board
        cells: list = self.model.art_board.arts[item_id].cells_array1d()
        self.model.art_board.delete_art(item_id)

        # Change current model-art_board
        self.model.art_board.index = self.model.art_board.count() - 1
        self.model.art_board.art.change_cells(cells)

        # Change cells in art board
        self.component_art_board.clear_cells_text()
        self.component_art_board.set_cells_text(cells)

    def _copy_image_carousel_item(self, item_id: int):
        """
            [temporarily method]

            TODO:
                - replace this method to menu
        """

        cells: list = self.model.art_board.arts[item_id].cells_array1d()
        image = self.api_draw_table.draw_table(cells=cells)
        self.component_carousel_of_images.add_carousel_item_pixmap(self._pillow_image_to_pixmap(image))
        self.component_carousel_of_images.update_items_title()

        self.model.art_board.arts[self.model.art_board.index].change_cells(cells)
        self.model.art_board.add_art(*self.component_art_board.table_size())
        self.model.art_board.index = self.model.art_board.count() - 1


class ControllerWorkspace(
    DefaultController,
    _ControllerArtBoard,
    _ControllerEmojiStore,
    _ControllerEmojiHistory,
    _ControllerCarouselOfImages
):
    """ Controller for 'ViewWorkspace' """

    def __init__(self, view: ViewWorkspace, model: ModelArt, model2: ModelEmojiHistory):
        self.register_controller(name='controller_workspace')
        self.clipboard = QGuiApplication.clipboard()

        # [ art-board ]
        model.resize.size_id = 1
        model.art_board.add_art(
            view.component_art_board.columnCount(),
            view.component_art_board.rowCount()
        )

        # [ controllers ]
        _ControllerArtBoard.__init__(self, view=view, model=model, clipboard=self.clipboard)
        view.component_art_board.update_size(size=model.resize.size)

        # [ emoji-store ]
        _ControllerEmojiStore.__init__(self, view=view, model2=model2, clipboard=self.clipboard)

        # [ emoji-history ]
        _ControllerEmojiHistory.__init__(self, view=view, model2=model2, clipboard=self.clipboard)

        # [ carousel-of-images ]
        _ControllerCarouselOfImages.__init__(self, view=view, model=model)

        # [ shortcuts ]
        _shortcuts: tuple = (
            QShortcut(QKeySequence(SETTINGS_SHORTCUTS['ClearCurrentArtBoard']['shortcut']), self.view),
            QShortcut(QKeySequence(SETTINGS_SHORTCUTS['AddCarouselItem']['shortcut']), self.view),
            QShortcut(QKeySequence(SETTINGS_SHORTCUTS['SaveFrames']['shortcut']), self.view)
        )

        _shortcuts[0].activated.connect(self.on_press_shortcut_clear_current_art_board)
        _shortcuts[1].activated.connect(self.on_press_shortcut_add_carousel_item)
        _shortcuts[2].activated.connect(self._on_press_shortcut_save_frames)

    def _on_press_shortcut_save_frames(self):
        if self.model.is_valid_filepath():
            api_export_frames(filepath=self.model.filepath, frames=self.model.art_board.arts)
            self.view.show_toast_message(title='Complete', message='Complete file save', duration=2000)
            return

        file: str = QFileDialog().getSaveFileName(
            self.view,
            "Save file",
            "",
            "JSON Files (*.json);;All Files (*)"
        )[0]

        try:
            api_export_frames(filepath=file, frames=self.model.art_board.arts)
            self.model.filepath = file
            self.view.show_toast_message(title='Complete', message='Complete file save', duration=2000)
        except FileNotFoundError as error:
            self.view.show_toast_message(title='Error', message='File not found: ' + str(error), duration=5000)

    def on_click_shortcuts_item(self, event, item: QPushButton):
        self.view.show_messagebox(title=item.text(), message=SETTINGS_SHORTCUTS_HTML[item.toolTip()], status='i')
