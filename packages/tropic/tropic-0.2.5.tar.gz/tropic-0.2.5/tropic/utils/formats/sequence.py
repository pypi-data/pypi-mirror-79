"""Type casting module."""


def lst2str(inp, sep='.'):
    """Hensel decode function.

    Args:
        inp (int): scalar to be represented as hensel code
        sep (str): base of encoding

    Returns:
        str: list of coefficients of hensel code
    """
    return sep.join(map(str, inp))
