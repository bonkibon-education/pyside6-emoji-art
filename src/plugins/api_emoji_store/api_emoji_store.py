"""
    Api: https://emoji-api.com/#documentation
    A free emoji API sourced directly from unicode.org - always up to date.
"""

import requests
from time import sleep
from json import dump, load


class _EmojiApi:
    def __init__(self, url: str, api_key: str):
        self._url: str = url
        self._api_key: str = api_key

    def api_get_categories(self) -> str | list | dict:
        return self._api_response(path='/categories', params={'access_key': self._api_key})

    def api_get_emojis_in_category(self, category: str) -> str | list | dict:
        data = self._api_response(path=f'/categories/{category}', params={'access_key': self._api_key})
        return data

    def _api_response(self, path: str, params: dict) -> str | list | dict:
        response = requests.get(url=self._url + path, params=params)
        return response.json() if response.status_code == 200 else f'Error {response.status_code}: {response.text}'


class _JsonAdapterEmojiStore:
    def __init__(self):
        super().__init__()
        self._filename = 'emoji-store.json'

    def write(self, date: dict):
        with open(file=self._filename, mode='w', encoding='utf-8') as file:
            dump(
                obj=date,
                fp=file,
                indent=2,
                ensure_ascii=False,
            )

    def read(self) -> dict:
        with open(file=f'plugins/api_emoji_store/{self._filename}', mode='r', encoding='utf-8') as file:
            return load(fp=file)

    @staticmethod
    def read_fix_double_emoji():
        with open(file=f'plugins/api_emoji_store/emoji-store-fix-double-emoji.json', mode='r', encoding='utf-8') as file:
            return load(fp=file)


def create_json_file(api_key: str) -> None:
    response_data: dict = dict()
    emoji_api = _EmojiApi(url='https://emoji-api.com/', api_key=api_key)
    api_request_get_categories: tuple = tuple(emoji_api.api_get_categories())

    for categories in api_request_get_categories:
        response_data[categories['slug']]: dict = {subcategory: list() for subcategory in categories['subCategories']}
        api_request_get_emojis: str | list | dict = emoji_api.api_get_emojis_in_category(category=categories['slug'])

        if not isinstance(api_request_get_emojis, list):
            continue

        for emoji in api_request_get_emojis:
            response_data[emoji['group']].setdefault(
                emoji['subGroup'], list()).append(
                {
                    'slug': emoji['slug'],
                    'character': emoji['character'],
                    'unicodeName': emoji['unicodeName'],
                    'codePoint': emoji['codePoint']
                }
            )

        sleep(2)

    json_adapter = _JsonAdapterEmojiStore()
    json_adapter.write(date=response_data)


def read_json_file() -> dict:
    json_adapter = _JsonAdapterEmojiStore()
    return json_adapter.read_fix_double_emoji()
