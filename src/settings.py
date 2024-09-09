from json import load, JSONDecodeError
from random import choice
from paths import path_read_file
from PySide6.QtWidgets import QMessageBox


def __settings_shortcuts_html(shortcut: str, desc: str):
    return f'<font color="#50C878" style="font-size: 14px; font-weight: 600;">[{shortcut}]</font>' \
           f'<font color="white" style="font-size: 14px;"> - {desc}</font>'


SETTINGS_MESSAGEBOX_ICON: dict = {
    'd': QMessageBox.Icon.NoIcon,
    'e': QMessageBox.Icon.Critical,
    'i': QMessageBox.Icon.Information,
    '?': QMessageBox.Icon.Question,
    '!': QMessageBox.Icon.Warning,
}

SETTINGS_WELCOME_EMOJI: str = choice(
    (
        '😎', '🥰', '💗',
        '😍', '🥰', '🤩',
        '🤪', '😱', '😇',
        '😈', '😼', '🐍'
    )
)


SETTINGS_SHORTCUTS: dict = path_read_file('app-shortcuts.json')

SETTINGS_SHORTCUTS_HTML: dict = {
    item[0]: __settings_shortcuts_html(item[1]['shortcut'], item[1]['description'])
    for item in SETTINGS_SHORTCUTS.items()
}
