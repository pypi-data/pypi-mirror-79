
import ujson
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from tabulate import tabulate


def to_table(data, tablefmt="fancy_grid", missingval="?"):
    headers = []
    if isinstance(data, list):
        headers = data[0].keys()
        values = [item.values() for item in data]
    elif isinstance(data, dict):
        headers = data.keys()
        values = data.values()

    headers = [col.replace("_", " ").title() for col in headers]
    return "\n" + tabulate(values, headers=headers,
                        missingval=missingval, tablefmt=tablefmt)


def to_json(obj):
    json_str = ujson.dumps(obj, indent=4, sort_keys=True)
    return "\n" + highlight(json_str, JsonLexer(), TerminalFormatter())


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
