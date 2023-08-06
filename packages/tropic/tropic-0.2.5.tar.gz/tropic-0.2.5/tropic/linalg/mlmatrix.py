"""Multi-level matrix core."""

import numpy
import tensorflow as tf
from tabulate import tabulate


def init(shape):
    """Do counting of number of levels of mutli-level matrix.

    Args:
        shape (tuple): shape of a new tensor

    Returns:
        tensor: new tensor filled with zeros
    """
    return tf.zeros(shape, dtype=tf.float32)


def pretty(inp):
    """Do pretty printing of mutli-level matrix.

    Args:
        inp (tensor): mutli-level matrix

    Returns:
        str: pretty string representation
    """
    if levels(inp) > 0:
        rows, cols = inp.shape[:2]
        table = numpy.ndarray((rows, cols), dtype=object)
        for row in range(rows):
            for col in range(cols):
                table[row, col] = pretty(inp[row, col])
        return tabulate(table, tablefmt=_format(inp))
    return _signum(inp) + str(inp.numpy())


def levels(matrix):
    """Do counting of number of levels of mutli-level matrix.

    Args:
        matrix (tensor): odd-dimensional tensor

    Returns:
        int: number of levels
    """
    return int(len(matrix.shape) / 2)


def random(shape):
    """Create random mutli-level matrix.

    Args:
        shape (tuple): shape of a matrix

    Returns:
        tensor: random matrix
    """
    matrix = tf.random.uniform(shape, minval=0, maxval=10, dtype=tf.int32)
    return tf.cast(matrix, dtype=tf.float32)


def _format(inp):
    return 'plain' if levels(inp) % 2 else 'grid'


def _signum(inp):
    return '-' if numpy.sign(inp.numpy()) == -1 else ''
