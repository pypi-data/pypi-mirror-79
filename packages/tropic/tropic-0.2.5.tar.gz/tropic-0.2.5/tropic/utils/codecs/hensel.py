"""Hensel encoder/decoder module."""


def encode(inp, base):
    """Hensel decoding function.

    Args:
        inp (list): list of p-adic coefficients
        base (int): base of p-adic encoding

    Returns:
        int: Hensel encoding
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
    elif abs(inp) == float('inf'):
        out += [inp]
    else:
        while inp:
            out += [int(abs(inp) % base)]
            inp //= base
        out.reverse()
    pads = [0 for _ in range(prec - len(out))]
    return pads + out
