import json

class DataUtils:
    def __init__(self):
        pass

    def append_data(self, chars, result, file):
        with open(file, 'r') as json_file:
            data = json.load(json_file)

        new_data = {
            'characters' : chars,
            'result' : result
        }

        data.append(new_data)

        with open(file, 'w') as json_file:
            json.dump(data, json_file, indent = 4)