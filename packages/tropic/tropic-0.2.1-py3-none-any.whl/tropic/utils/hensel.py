"""Hensel encoder/decoder module."""

import ast

from tropic.common.constants import oo


def encode(inp, base):
    """Hensel decoding function.

    Args:
        inp (list): list of p-adic coefficients
        base (int): base of p-adic encoding

    Returns:
        int: hensel code
    """
    rinp = enumerate(reversed(inp))
    monomials = [coef * base ** power for power, coef in rinp]
    return sum(monomials)


def decode(inp, base, prec=-1):
    """Hensel decoding function.

    Args:
        inp (int): scalar to be represented as hensel code
        base (int): base of encoding
        prec (int): positive integer, the p-adic precision of the root

    Returns:
        list: list of coefficients of hensel code
    """
    out = []
    if inp in {0, 1}:
        out += [inp]
    elif abs(inp) == oo:
        out += [inp]
    else:
        while inp:
            out += [int(abs(inp) % base)]
            inp //= base
        out.reverse()
    pads = [0 for _ in range(prec - len(out))]
    return pads + out


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
