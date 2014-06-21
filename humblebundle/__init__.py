__author__ = "Joel Pedraza"
__copyright__ = "Copyright 2014, Joel Pedraza"
__license__ = "MIT"
__all__ = ['HumbleApi', 'logger']

from humblebundle.client import HumbleApi
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())