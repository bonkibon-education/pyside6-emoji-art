import json


with open(file='emoji-art.json', mode='r', encoding='utf-8') as file:
    data: dict = json.load(fp=file)

    for i in range(data['frames']):
        print(data[f'frame:{i}']['text'])
        print()
