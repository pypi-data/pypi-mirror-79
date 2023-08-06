"""Type casting module."""

import ast

from tropic.common.const import oo


def num2str(inp):
    """Hensel decode function.

    Args:
        inp (int): scalar to be represented as hensel code

    Returns:
        str: list of coefficients of hensel code
    """
    sgn = '-' if inp < 0 else '+'
    pinp = abs(inp)
    return ''.join([sgn, 'oo']) if pinp == oo else str(inp)


def str2num(inp):
    """Hensel decode function.

    Args:
        inp (int): scalar to be represented as hensel code

    Returns:
        float: list of coefficients of hensel code
    """
    sgn = '-' if inp < 0 else ''
    inf = ''.join([sgn, 'oo'])
    return inf if abs(inp) == oo else str(inp)


def lst2str(inp, sep='.'):
    """Hensel decode function.

    Args:
        inp (int): scalar to be represented as hensel code
        sep (str): base of encoding

    Returns:
        str: list of coefficients of hensel code
    """
    return sep.join(map(str, inp))


def str2lst(inp):
    """Hensel decode function.

    Args:
        inp (str): scalar to be represented as hensel code

    Returns:
        str: list of coefficients of hensel code
    """
    return map(float, ast.literal_eval(inp))
