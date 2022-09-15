import sys
from pprint import pprint
import traceback
from collections import namedtuple
from datetime import datetime


def pk(*args):
    print(";; {}".format(args), file=sys.stderr)
    return args[-1]


def ppk(*args):
    pprint(";; {}".format(args), file=sys.stderr)
    return args[-1]


def check():
    print("* Check check @ {} @ {}".format(__file__, datetime.now().isoformat()))
    for key, object in globals().items():
        if key.startswith('_check_'):
            assert callable(object)
            print("** Check: {}".format(key))
            try:
                object()
            except AssertionError as exc:
                print("*** AssertionError!")
                traceback.print_exception(exc)
                sys.exit(1)
            except Exception as exc:
                print("*** Exception...")
                traceback.print_exception(exc)
                sys.exit(2)


def _check_000():
    assert True


Annotation = namedtuple('Annotation', 'offset line column')
XChar = namedtuple('XChar', 'char annotation')
Expr = namedtuple('Expression', 'expr type annotation')


def string2xchars(string):
    line = 0
    column = 0
    for offset, char in enumerate(string):
        char = string[offset]

        yield XChar(char, Annotation(offset, line, column))

        if char == '\n':
            line += 1
            column = 0
        else:
            column += 1


def _check_001():
    given = """a

z"""
    expected = (
        XChar('a', Annotation(0, 0, 0)),
        XChar('\n', Annotation(1, 0, 1)),
        XChar('\n', Annotation(2, 1, 0)),
        XChar('z', Annotation(3, 2, 0))
    )

    out = tuple(string2xchars(given))

    assert out == expected


def inext(g):
    # XXX: TODO: Quick hack?!
    try:
        return next(g)
    except StopIteration:
        return None


def read(string):
    xchars = string2xchars(string)
    xchar = inext(xchars)
    return _read(xchar, xchars)[1]


DELIMITERS = set('"() \n')


def _read_string(annotation, xchars):
    out = ''
    for xchar in xchars:
        match xchar.char:
            case '"':
                return inext(xchars), Expr(out, str, annotation)
            case '\\':
                # TODO: xchars raise StopIteration
                xchar = inext(xchars)
                match xchar.char:
                    case '"':
                        out += '"'
                    case _:
                        xchar = inext(xchars)
                        out += chr('\\{}'.format(xchar))
            case _:
                out += xchar.char

    raise NotImplementedError()


symbol = pk('symbol is object @ ', object())


def _read_number_or_symbol(xchar, xchars):
    annotation = xchar.annotation
    out = xchar.char
    for xchar in xchars:
        if xchar.char in DELIMITERS:
            break

        out += xchar.char

    for type in (int, float):
        try:
            return xchar, Expr(type(out), type, annotation)
        except ValueError:
            continue

    return xchar, Expr(out, symbol, annotation)


def _read(xchar, xchars):
    while True:
        # if xchar is space in between expressions ie. not inside #
        # double quotes, then it is ignored.
        if xchar.char.isspace():
            xchar = inext(xchars)
            continue

        match xchar.char:
            case '(':
                annotation = xchar.annotation
                out = []
                xchar = inext(xchars)
                while True:
                    # TODO: retry operator walrus with a tuple
                    xchar, expr = _read(xchar, xchars)
                    if expr == ')':
                        return xchar, Expr(tuple(out), tuple, annotation)
                    out.append(expr)
            case ')':
                return inext(xchars), ')'
            case '"':
                return _read_string(xchar.annotation, xchars)
            case _:
                return _read_number_or_symbol(xchar, xchars)


def _check_002():
    assert read("cosmit") == ("cosmit", symbol, (0, 0, 0))


def _check_003():
    assert read("2006") == (2006, int, (0, 0, 0))


def _check_004():
    assert read("3.1415") == (3.1415, float, (0, 0, 0))


def _check_005():
    assert read(""" "azul felawun" """) == ("azul felawun", str, (1, 0, 1))


def _check_006():
    input = """(hello
world
42
1337
3.1415
"ar tafath"

)
"""
    match read(input):
        # XXX: I do not know how to match expr.type...
        case Expr((("hello", _, _),
                   ("world", _, _),
                   (42, _, _),
                   (1337, _, _),
                   (3.1415, _, _),
                   ("ar tafath", _, _)),
                  _,
                  _):
            assert True
        case _:
            assert False


def write(expr):
    # XXX: pattern matching on types is difficult, possibly a scoping
    # issue.
    if expr.type is int:
        return str(expr.expr)
    elif expr.type is float:
        return str(expr[0])
    elif expr.type is str:
        # TODO: output must be readable, hence requires to use the
        # escape char anti-slash.
        return '"' + expr.expr + '"'
    elif expr.type is tuple:
        return '(' + " ".join(write(x) for x in expr.expr) + ')'
    elif expr.type is symbol:
        return expr.expr
    raise NotImplementedError()


def _check_007():
    expected = """(azul 1337 "amirouche" 3.1415)"""
    assert write(read(expected)) == expected


def _check_008():
    expected = """(azul (1337 "amirouche") 3.1415)"""
    assert write(read(expected)) == expected


def main():
    match sys.argv[1:]:
        case ['check']:
            check()


if __name__ == "__main__":
    main()
