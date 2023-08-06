from enum import Enum
from io import StringIO
from itertools import chain

from .. import iterutils
from .. import path
from .. import safe_str
from ..shell import posix as pshell

Syntax = Enum('Syntax', ['variable', 'shell'])


class Writer:
    def __init__(self, stream):
        self.stream = stream

    def write_literal(self, string):
        self.stream.write(string)

    def write(self, thing, syntax, shell_quote=pshell.quote_info):
        thing = safe_str.safe_str(thing)
        shelly = syntax == Syntax.shell
        escaped = False

        if isinstance(thing, safe_str.literal_types):
            escaped = True
            self.write_literal(thing.string)
        elif isinstance(thing, str):
            if shelly and shell_quote:
                thing, escaped = shell_quote(thing)
            self.write_literal(thing)
        elif isinstance(thing, safe_str.jbos):
            for i in thing.bits:
                escaped |= self.write(i, syntax, shell_quote)
        elif isinstance(thing, path.BasePath):
            out = Writer(StringIO())
            thing = thing.realize(path_vars, shelly)
            escaped = out.write(thing, syntax, pshell.inner_quote_info)

            thing = out.stream.getvalue()
            if shelly and escaped:
                thing = pshell.wrap_quotes(thing)
            self.write_literal(thing)
        else:
            raise TypeError(type(thing))

        return escaped

    def write_each(self, things, syntax, delim=safe_str.literal(' '),
                   prefix=None, suffix=None, shell_quote=pshell.quote_info):
        for i in iterutils.tween(things, delim, prefix, suffix):
            self.write(i, syntax, shell_quote)


class Variable(safe_str.safe_string_ops):
    def __init__(self, name):
        self.name = name

    def use(self):
        return safe_str.literal('${{{}}}'.format(self.name))

    def _safe_str(self):
        return self.use()

    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        return repr(self.use())

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, rhs):
        return self.name == rhs.name

    def __ne__(self, rhs):
        return not (self == rhs)


path_vars = {i: Variable(i.name) for i in chain(
    [path.Root.srcdir, path.Root.builddir], path.InstallRoot
)}
