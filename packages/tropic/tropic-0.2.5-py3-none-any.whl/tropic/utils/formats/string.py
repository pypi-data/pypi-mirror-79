"""Type casting module."""

import ast


def to_list(inp):
    """Hensel decode function.

    Args:
        inp (str): scalar to be represented as hensel code

    Returns:
        str: list of coefficients of hensel code
    """
    return map(float, ast.literal_eval(inp))
