from flask import request
import json

from .utils import AttrDict


class ParseError(BaseException):
    def __init__(self, message):
        self.message = message


class Argument(object):
    """
    :param name: name of option
    :param default: default value if the argument if absent
    :param bool required: is required
    """

    def __init__(self, name, default=None, required=True, type=str, filter=None, help=None, nullable=False):
        self.name = name
        self.default = default
        self.type = type
        self.required = required
        self.nullable = nullable
        self.filter = filter
        self.help = help
        if not isinstance(self.name, str):
            raise TypeError('Argument name must be string')
        if filter and not callable(self.filter):
            raise TypeError('Argument filter is not callable')

    def parse(self, has_key, value):
        if not has_key:
            if self.required and self.default is None:
                raise ParseError(
                    self.help or 'Required Error: %s is required' % self.name)
            else:
                return self.default
        elif value in [u'', '', None]:
            if self.default is not None:
                return self.default
            elif not self.nullable and self.required:
                raise ParseError(
                    self.help or 'Value Error: %s must not be null' % self.name)
            else:
                return None
        try:
            if self.type in (int, float, complex, bool):
                value = self.type(value)
            elif self.type in (list, dict):
                value = json.loads(value)
                assert isinstance(value, self.type)
            elif self.type == bool:
                assert value.lower() in ['true', 'false']
                value = value.lower() == 'true'
        except (ValueError, AssertionError):
            raise ParseError(self.help or 'Type Error: %s type must be %s' % (
                self.name, self.type))

        if self.filter:
            if not self.filter(value):
                raise ParseError(
                    self.help or 'Value Error: %s filter check failed' % self.name)
        return value


class BaseParser(object):
    def __init__(self, *args):
        self.args = []
        for e in args:
            if isinstance(e, str):
                e = Argument(e)
            elif not isinstance(e, Argument):
                raise TypeError('%r is not instance of Argument' % e)
            self.args.append(e)

    def _get(self, key):
        raise NotImplementedError

    def _init(self, data):
        raise NotImplementedError

    def add_argument(self, **kwargs):
        self.args.append(Argument(**kwargs))

    def parse(self, data=None):
        rst = AttrDict()
        try:
            self._init(data)
            for e in self.args:
                rst[e.name] = e.parse(*self._get(e.name))
        except ParseError as err:
            return None, err.message
        return rst, None


class JsonParser(BaseParser):
    def __init__(self, *args):
        self.__data = None
        super(JsonParser, self).__init__(*args)

    def _get(self, key):
        return key in self.__data, self.__data.get(key)

    def _init(self, data):
        if data is None:
            self.__data = request.args.to_dict()
            post_json = request.get_json()
            if isinstance(post_json, dict):
                self.__data.update(post_json or {})
            return
        try:
            if isinstance(data, (str, bytes)):
                data = data.decode('utf-8')
                self.__data = json.loads(data)
            else:
                assert hasattr(data, '__contains__')
                assert hasattr(data, 'get')
                assert callable(data.get)
                self.__data = data
        except (ValueError, AssertionError):
            raise ParseError('Invalid data type for parse')
