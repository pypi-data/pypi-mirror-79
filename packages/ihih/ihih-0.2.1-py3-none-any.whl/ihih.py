#!/usr/bin/python
'''ihih - simple configuration parsers with dictionary-like interface

:Source code: `GitLab project <https://gitlab.com/romain-dartigues/python-ihih>`_
:License: `BSD 3-Clause <http://opensource.org/licenses/BSD-3-Clause>`_
'''

# stdlib
import errno
import io
import os
import re
import sys





__version__ = '0.2.1'

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

STRING_TYPES = (str, )
text_type = str # pylint: disable=invalid-name

if PY2:
    STRING_TYPES = (basestring, str, unicode) # pylint: disable=undefined-variable
    text_type = unicode # pylint: disable=invalid-name,undefined-variable





class IHIH(dict): # pylint: disable=too-many-instance-attributes
    '''IHIH - simple configuration parser

    One key/value pair per line.
    '''
    ignore_errors = False
    '''do not stop on OSError when reading sources'''

    encoding = 'utf8'
    '''define the encoding'''

    _escape = r'(?<!\\)(?:\\\\)*'
    '''regexp definition of the escape sequence'''

    _escaped_chars = r'[\\\'\"\#/\\]'
    '''regexp definition of characters to unconditionally un-escape'''

    _escaped = r'(?:\\)(?P<char>%s)'

    _comment = r'(\s*%(escape)s(?:\#|//))'
    '''regexp definition of an in-line comment'''

    _separator = r'\='
    '''regexp definition of key/value separator

    Must be a fixed-width expression.'''

    _extract = r'''^\s*
        (?P<key>.+?)
        \s*%(separator)s\s*
        (?P<value>.*)'''
    '''extract ``key = [value]`` on a single line'''

    _quote = r'["\']'
    '''define what a quote might be'''

    _quoted = r'%(escape)s(?P<quote>%(quote)s)(?P<value>.*?)%(escape)s(?P=quote)'
    '''how to find a quoted value'''

    _bool = r'^(?P<false>0|no|false|off|disabled)|(?P<true>1|yes|true|on|enabled)$'
    'regexp definition of a boolean value (used by :meth:`get_bool`)'


    # pylint: disable=keyword-arg-before-vararg
    def __init__(self, filenames, ignore_errors=False, *args, **kwargs):
        '''attempt to parse a list of filenames

        :param filenames: one or many path to files
        :type filenames: str or list(str)
        :param bool ignore_errors: fail silently on :py:exc:`~exceptions.OSError`
        :param list args: passed to :py:class:`dict` constructor
        :param dict kwargs: passed to :py:class:`dict` constructor
        '''
        dict.__init__(self, *args, **kwargs)

        self._comment = self._comment % {
            'escape': self._escape,
        }
        self.r_comment = re.compile(self._comment)
        self.r_extract = re.compile(
            self._extract % {
                'separator': self._separator,
            },
            re.X
        )
        self.r_quoted = re.compile(
            self._quoted % {
                'escape': self._escape,
                'quote': self._quote,
            }
        )
        self.r_escaped = re.compile(
            self._escaped % self._escaped_chars
        )
        self.r_bool = re.compile(self._bool, re.I)

        if isinstance(filenames, STRING_TYPES):
            self.__source = (os.path.realpath(filenames),)
        else:
            self.__source = tuple(
                os.path.realpath(filename)
                for filename in filenames
            )

        self.__mtime = {}

        self.ignore_errors = ignore_errors
        self.reload()


    def reload(self, force=False, ignore_errors=None):
        '''call :meth:`parse` on each configuration file

        :param bool force: force (re)loading of files
        :param bool ignore_errors: ignore unreadable files
        :return: None
        '''
        for filename in self.__source:
            self.parse(filename, force, ignore_errors)


    def parse(self, filename, force=False, ignore_errors=None):
        '''parse a configuration file

        :param str filename: path to file to parse
        :param bool force: force (re)loading of files
        :param bool ignore_errors: ignore unreadable files,
                                   default: :attr:`ignore_errors`
        :return: bool

        .. Note::
           `filename` should be an absolute path.
        '''
        if ignore_errors is None:
            ignore_errors = self.ignore_errors

        try:
            mtime = os.stat(filename).st_mtime
        except OSError as error:
            if error.errno == errno.ENOENT or ignore_errors:
                # file not found...
                return False
            raise

        if mtime <= self.__mtime.get(filename, 0) and not force:
            # file did not change
            return None

        try:
            with io.open(filename, 'r', encoding=self.encoding) as fobj:
                for line in fobj:
                    results = self.r_extract.match(line)
                    if results:
                        self[results.group('key')] = results \
                            .group('value').rstrip()
        except (OSError, IOError):
            if ignore_errors:
                return False
            raise

        self.__mtime[filename] = mtime

        return True


    def _unescape(self, value, quote=None): # pylint: disable=unused-argument
        '''remove escape prefix on "known escape"

        See :attr:`_escaped_chars`.

        This method attempt to utf8 encode :py:func:`unicode` objects.
        '''
        data = text_type()
        escaped = None
        prev = 0

        for escaped in self.r_escaped.finditer(value):
            if escaped.start() > prev:
                data += value[prev:escaped.start()]

            data += escaped.group('char')
            prev = escaped.end()

        if escaped and escaped.end() < len(value):
            data += value[escaped.end():]

        elif not escaped:
            data += value

        return data


    def _handle_fragment(self, fragment, quote=None):
        '''handle a fragment of a value

        Provided to help on subclassing.'''
        return self._unescape(fragment, quote)


    def _comment_at(self, value):
        'return the position of the begining of a comment'
        comment = self.r_comment.search(value)
        return comment and comment.start()


    def _parse_value(self, value, data):
        '''parse the "value" part of a "key / value"

        This function handle the quoted parts and the comments.

        :param str value: value to parse
        :param data: instance supporting ``+=`` operator
        :return: parsed value
        :rtype: type of `data`
        '''
        quoted = None
        prev = 0

        for quoted in self.r_quoted.finditer(value):
            if quoted.start() > prev:
                # unquoted part before a quoted fragment
                comment_at = self._comment_at(
                    value[prev:quoted.start()]
                )
                data += self._handle_fragment(
                    value[
                        prev
                        :
                        quoted.start()
                        if comment_at is None
                        else comment_at
                    ]
                )
                if comment_at is not None:
                    break

            # quoted fragment
            data += self._handle_fragment(
                quoted.group('value'),
                quoted.group('quote')
            )
            prev = quoted.end()

        if quoted and quoted.end() < len(value):
            # there is unquoted string after the quoted one
            data += self._handle_fragment(
                value[
                    quoted.end()
                    :
                    self._comment_at(value[quoted.end():])
                ]
            )

        elif not quoted:
            # nothing was quoted
            data += self._handle_fragment(
                value[:self._comment_at(value)]
            )

        return data


    def __contains__(self, key):
        '''True if self contains `key`

        .. Note::
           The `key` will be casted as :func:`text_type`.
        '''
        return dict.__contains__(self, text_type(key))


    def __setitem__(self, key, value):
        '''set item `key` to `value`

        .. Note::
           The `key` will be casted as :func:`text_type`.
        '''
        return dict.__setitem__(
            self,
            text_type(key),
            self._parse_value(
                text_type(value),
                text_type()
            )
        )


    def __getitem__(self, key):
        '''return `key` value as internal type

        You probably want to use one of the following:
        :meth:`get_text`, :meth:`get_float`, :meth:`get_int`.

        .. Note::
           The `key` will be casted as :func:`text_type`.
        '''
        return dict.__getitem__(self, text_type(key))


    def __delitem__(self, key):
        '''delete `key` from dict

        .. Note::
           The `key` will be casted as :func:`text_type`.
        '''
        return dict.__delitem__(self, text_type(key))


    def get_text(self, key, default=None):
        '''return `key` value as :func:`text_type`
        or `default` if not found

        .. Note::
           The `key` will be casted as :func:`text_type`.
        '''
        if key in self:
            return text_type(self[key])
        return default


    get = get_text
    '''alias to :meth:`get_text`'''


    def get_float(self, key, default=None, errors='strict'):
        '''return `key` value as :py:func:`float` or `default`
        if not found

        If `errors` is "ignore", return `default` value instead of
        raising :py:exc:`~exceptions.ValueError` on failure.

        .. Note::
           The `key` will be casted as :func:`text_type`.
        '''
        if key in self:
            try:
                return float(self[key])
            except ValueError:
                if errors != 'ignore':
                    raise
        return default


    def get_int(self, key, default=None, errors='strict', base=10):
        '''return `key` value as :py:func:`int` or `default`
        if not found

        If `errors` is "ignore", return `default` value instead of
        raising :py:exc:`~exceptions.ValueError` on failure.

        .. Note::
           The `key` will be casted as :func:`text_type`.
        '''
        if key in self:
            try:
                return int(self.get_text(key), base)
            except ValueError:
                if errors != 'ignore':
                    raise
        return default


    def get_bool(self, key, default=None):
        '''attempt to coerce `key` value to a boolean
        accordingly :attr:`_bool` rules
        '''
        if key in self:
            match = self.r_bool.search(self.get_text(key))
            if match:
                return bool(match.group('true'))
        return default



class IHIHI(IHIH):
    '''IHIH Interpolate - :class:`IHIH` with variable interpolation
    '''

    _variable = r'%(escape)s\$(?P<value>\w+|%(escape)s\{(?P<unquoted>.+?)%(escape)s\})'
    '''regexp definition of a "variable"'''

    _escaped_chars = r'[\\\'\"\#/\\\$\{\}]'
    '''regexp definition of characters to unconditionally un-escape'''

    def __init__(self, *args, **kwargs):
        self.r_variable = re.compile(
            self._variable % {'escape': self._escape},
            re.UNICODE
        )

        super(IHIHI, self).__init__(*args, **kwargs)


    def __setitem__(self, key, value):
        return dict.__setitem__(
            self,
            text_type(key),
            self._parse_value(
                text_type(value),
                []
            )
        )


    def _handle_fragment(self, fragment, quote=None):
        '''search for variables in `fragment`'''
        var = None
        data = []
        prev = 0

        if quote in (None, '"'):
            for var in self.r_variable.finditer(fragment):
                if var.start() > prev:
                    data.append((
                        self._unescape(
                            fragment[prev:var.start()],
                            quote
                        ),
                        False
                    ))

                data.append((
                    self._unescape(
                        var.group('unquoted')
                        if var.group('unquoted')
                        else var.group('value')
                    ),
                    True
                ))

                prev = var.end()

        if var and var.end() < len(fragment):
            data.append((self._unescape(fragment[var.end():], quote), False))

        elif not prev:
            data = ((self._unescape(fragment, quote), False),)

        return data


    def __getkey(self, key, path=None):
        '''return `key` value as internal type
        with interpolated variables

        For more informations, see: :meth:`~IHIH.__getitem__`.
        '''
        if path is None:
            path = []
        path.append(key)
        data = super(IHIHI, self).__getitem__(key)
        value = text_type()

        for sub, is_variable in data:
            if is_variable:
                if sub not in self:
                    continue
                if sub in path:
                    value += self._recursive(sub)

                else:
                    value += self.__getkey(sub, path)
            else:
                value += sub

        path.remove(key)
        return value


    def __getitem__(self, key):
        return self.__getkey(key)


    def _recursive(self, value): # pylint: disable=no-self-use,unused-argument
        '''recursive variable handler

        Default: empty string

        You can overwrite this function when subclassing
        and chose to return a unexpended version of the variable,
        raise an error or make a single, non recursive, lookup.
        '''
        return ''
