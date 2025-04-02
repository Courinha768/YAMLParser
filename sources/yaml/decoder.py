from base64 import decode
from types import MappingProxyType
from typing import Mapping, Any

from django.utils.text import normalize_newlines
from jinja2.utils import generate_lorem_ipsum

class YAMLDecodeError(ValueError):
    """Subclass of ValueError with the following additional properties:

    msg: The unformatted error message
    doc: The YAML document being parsed
    pos: The start index of doc where parsing failed
    lineno: The line corresponding to pos
    colno: The column corresponding to pos

    """
    def __init__(self, msg, doc, pos):
        lineno = doc.count('\n', 0, pos) + 1
        colno = pos - doc.rfind('\n', 0, pos)
        errmsg = '%s: line %d column %d (char %d)' % (msg, lineno, colno, pos)
        ValueError.__init__(self, errmsg)
        self.msg = msg
        self.doc = doc
        self.pos = pos
        self.lineno = lineno
        self.colno = colno

    def __reduce__(self):
        return self.__class__, (self.msg, self.doc, self.pos)

def get_indent(s : str):
    return len(s) - len(s.lstrip())

def get_key_and_value(s : str):
    splited = s.split(':', 1)

    key   : str = splited[0].strip().strip('\"')
    value : Any = splited[1].strip().strip('\"') if len(splited) > 1 else ''

    if value == 'false':
        value = False
    elif value == 'true':
        value = True
    elif value == 'null':
        value = None
    elif value.isnumeric():
        value = float(value)

    return key, value


IGNORED_LINES = ['', '---']
EOF = '...'

class YAMLDecoder(object):
    """
    Simple YAML decoder
    """

    def __init__(self):
        self.gnl_s : dict[str, list[str]] = dict({'': ['...']})
        self.gnl_index : dict[str, int] = dict({'': 0})

    def setup_new_document(self, s):
        self.gnl_s[s] = s.split('\n')
        self.gnl_s[s].append('...')
        self.gnl_index[s] = 0

    def get_next_line(self, s):
        if s not in self.gnl_index or s not in self.gnl_s:
            self.setup_new_document(s)

        line : str = ''
        while line.strip() == '' or line.lstrip().startswith('#'):
            line = self.gnl_s[s][self.gnl_index[s]]
            if line != EOF:
                self.gnl_index[s] += 1
        return line

    def check_next_line(self, s, depth : int = 0):
        if s not in self.gnl_index:
            self.setup_new_document(s)

        line : str = self.gnl_s[s][self.gnl_index[s] + depth]
        while line.strip() == '' or line.lstrip().startswith('#'):
            self.gnl_index[s] += 1
            line = self.gnl_s[s][self.gnl_index[s] + depth]
        return line

    def decode(self, s : str, stack : dict = None) -> Any:
        next_line = self.check_next_line(s)
        indent = get_indent(next_line)

        if next_line.strip().startswith('- '):
            return self.decode_list(s, indent)
        else:
            return self.decode_object(s, indent, stack)


    def decode_object(self, s : str, indent : int, stack : dict = None) -> dict:
        if stack is None:
            stack = {}

        while True:
            line = self.get_next_line(s)
            if line == EOF or get_indent(line) < indent:
                break

            key, value = get_key_and_value(line)

            if value != '':
                stack[key] = value
            else:
                stack[key] = self.decode(s)

        return stack

    def decode_list(self, s : str, indent : int) -> list:
        stack = []

        while True:
            line = self.get_next_line(s)
            if line == EOF or get_indent(line) < indent:
                break

            line = line.strip().lstrip('- ')

            if ':' in line:
                key, value = get_key_and_value(line)

                stack.append(self.decode(s, {key: value if value != '' else self.decode(s)}))
            else:
                stack.append(line if not line.isnumeric() else float(line))

        return stack