from glob import glob
from pathlib import Path
from os.path import splitext
from json import loads

"""
PATHS_STRUCTURE: dict = {
    'css': 'src/assets/css',
    'html': 'src/assets/html',
    'json': 'src/assets/json',
    'controllers': 'src/controllers',
    'layouts': 'src/layouts',
    'models': 'src/models'
}
"""


PATH_FOLDERS: dict[str: list] = dict({
    Path(directories).name: [
        file for file in Path(directories).glob('*')
    ] for directories in glob('**/', recursive=True)
})

PATH_FILES_EXTENSION: set = set({
    splitext(path)[1] for path in glob('**/*', recursive=True)
    if splitext(path)[1]
})

PATH_FILES: dict[str: list] = dict({
    extension: [
        Path(file) for file in glob('**/*', recursive=True) if file.endswith(extension)
    ] for extension in PATH_FILES_EXTENSION
})


__cache_read_store: dict = dict()


def read_html_file(path) -> str:
    with open(path, encoding='utf-8', mode='r') as file:
        return file.read()


def read_json_file(path) -> dict:
    with open(path, encoding='utf-8', mode='r') as file:
        return loads(file.read())


def read_text_file(path) -> str:
    with open(path, encoding='utf-8', mode='r') as file:
        return ' '.join(file.read().rsplit())


def path_read_file(file: str) -> str | dict:
    extension: str = splitext(file)[1]

    if extension not in PATH_FILES_EXTENSION:
        return ""

    for path in PATH_FILES[extension]:
        if path.name != file:
            continue
        if path in __cache_read_store:
            return __cache_read_store[path]

        if extension == '.html':
            content = read_html_file(path)
        elif extension == '.json':
            content = read_json_file(path)
        else:
            content = read_text_file(path)

        __cache_read_store[path] = content
        return content
    return ""
