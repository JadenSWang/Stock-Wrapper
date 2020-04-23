import json

class JSONReader:
    @staticmethod
    def read_file(filename):
        with open(filename) as json_file:
            data = json.load(json_file)

        return data

    @staticmethod
    def write_file(filename, data):
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)