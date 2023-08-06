"""Logger module."""

import logzero

logzero.logfile('log.txt')


def log(inp):
    """Do info logging.

    Args:
        inp (str): string to be logged
    """
    logzero.logger.info(inp)
