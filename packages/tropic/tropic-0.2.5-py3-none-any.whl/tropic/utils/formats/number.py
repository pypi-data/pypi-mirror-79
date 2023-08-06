"""Type casting module."""


from tropic.engine.const import oo


def to_string(inp):
    """Do number conversion to string.

    Args:
        inp (float): scalar to be represented as hensel code

    Returns:
        str: list of coefficients of hensel code
    """
    return _sinf(inp) if abs(inp) == oo else str(inp)


def _ssign(inp):
    """Do string representation of the input value.

    Args:
        inp (float): scalar

    Returns:
        str: '-' or '+'
    """
    return '-' if inp < 0 else '+'


def _sinf(inp):
    """Do string representation of the infinity.

    Args:
        inp (float): scalar

    Returns:
        str: '-' or '+'
    """
    return ''.join([_ssign(inp), 'oo'])
