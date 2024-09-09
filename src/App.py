import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from paths import path_read_file
from settings import SETTINGS_WELCOME_EMOJI
from util import util_convert_text_to_pixmap

from models.ModelArt import ModelArt
from views.ViewWorkspace import ViewWorkspace
from models.ModelEmojiHistory import ModelEmojiHistory
from controllers.ControllerWorkspace import ControllerWorkspace


if __name__ == "__main__":
    # App
    app = QApplication(sys.argv)
    app.setStyleSheet(path_read_file('app.css'))
    app.setWindowIcon(QIcon(util_convert_text_to_pixmap(SETTINGS_WELCOME_EMOJI)))

    # View
    view_work_space = ViewWorkspace()
    view_work_space.setStyleSheet(path_read_file('workspace.css'))

    # Controller
    controller_work_space = ControllerWorkspace(
        view=view_work_space,
        model=ModelArt(),
        model2=ModelEmojiHistory()
    )

    view_work_space.bind_to_controller(controller=controller_work_space)

    # Show
    view_work_space.show()
    sys.exit(app.exec())
