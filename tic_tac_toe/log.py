import logging
import sys

from logging import INFO, DEBUG, CRITICAL, WARNING

logger = None
verbosity = logging.INFO

def get_logger() -> logging.Logger:
    global logger
    if logger is None:
        logger = logging.getLogger()
        logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger

def set_verbosity(verb: int):
    global verbosity
    verbosity = verb
    logger.setLevel(verbosity)
