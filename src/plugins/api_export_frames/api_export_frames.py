import datetime
from abc import abstractmethod
from dataclasses import dataclass
import json


@dataclass
class _ContractArtBoards:

    @abstractmethod
    def convert_to_text(self, replace_none: str):
        pass

    @abstractmethod
    def get_cells(self, only_value: bool):
        pass


def api_export_frames(filepath: str, frames: list[_ContractArtBoards]):
    output: dict = dict(frames=len(frames), date=datetime.datetime.now().__str__())

    for i, frame in enumerate(frames):
        output[f'frame:{i}'] = {
            'cells': frame.get_cells(only_value=True),
            'text': frame.convert_to_text(replace_none='▫️')
        }

    with open(file=filepath, encoding='utf-8', mode='w') as file:
        json.dump(output, fp=file, ensure_ascii=False, indent=4)
