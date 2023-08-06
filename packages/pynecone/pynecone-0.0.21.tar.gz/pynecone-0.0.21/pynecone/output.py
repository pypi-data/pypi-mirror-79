from tabulate import tabulate
import json


class OutputFormat:
    def __init__(self, type='table', header=['NAME'], rows=['name']):
        self.type = type
        self.header = header
        self.rows = rows


class Output:

    @classmethod
    def format(cls, output, output_format=OutputFormat()):
        if type(output) is list:
            return cls.format_items(output, output_format)
        else:
            return cls.format_item(output, output_format)

    @classmethod
    def extract_rows(cls, items, output_format):
        return [[i[r] for r in output_format.rows] for i in items]

    @classmethod
    def format_items(cls, items, output_format):
        if output_format.type == 'json':
            return json.dumps(items)
        else:
            return tabulate(cls.extract_rows(items, output_format), output_format.header)

    @classmethod
    def format_item(cls, item, output_format):
        if output_format.type == 'json':
            return json.dumps(item)
        else:
            return tabulate(cls.extract_rows(item, output_format), output_format.header)

    @classmethod
    def output(cls, data, path=None):
        if path:
            if isinstance(data, str):
                with open(path, 'w') as f:
                    print(data, file=f)
            else:
                with open(path, 'wb') as f:
                    f.write(data)
        else:
            print(data)