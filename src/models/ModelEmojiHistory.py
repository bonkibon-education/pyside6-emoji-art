from emoji import is_emoji

_LIMIT_ENTRY: int = 15


class DuplicateEntryError(Exception):
    pass


class LimitEntryError(Exception):
    pass


class ModelEmojiHistory:
    def __init__(self):
        self._entry: list[str] = []

    def insert_entry(self, entry: str, index: int = 0):
        self._validate_entry(entry)
        self._entry.insert(0, entry)
        return self._entry[index]

    def add_entry(self, entry: str):
        self._validate_entry(entry)
        return self._entry.append(entry)

    def del_entry(self, index: int):
        self._validate_index(index)
        del self._entry[index]

    def get_entry(self, index: int):
        self._validate_index(index)
        return self._entry[index]

    def get_entries(self):
        return self._entry

    def get_last_entry(self) -> tuple[str, int]:
        index: int = len(self._entry) - 1
        return self._entry[index], index

    def _validate_index(self, index: int):
        if not isinstance(index, int):
            raise ValueError(f'Invalid value type')
        if not (0 <= index < len(self._entry)):
            raise ValueError(f'Invalid range index')

    def _validate_entry(self, entry: str):
        if not isinstance(entry, str):
            raise ValueError(f'Invalid value type: {entry} (not type "str")')
        if not is_emoji(entry):
            print(entry)
            raise ValueError(f'Invalid value type: {entry} (not type "emoji")')
        if entry in self._entry:
            raise DuplicateEntryError(f'Duplicate value: {entry} in {self._entry}')
        if len(self._entry) >= _LIMIT_ENTRY:
            raise LimitEntryError(f'Limit value: len({self._entry}) >= {_LIMIT_ENTRY}')