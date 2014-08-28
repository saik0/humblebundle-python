__author__ = "Joel Pedraza"
__copyright__ = "Copyright 2014, Joel Pedraza"
__license__ = "MIT"

from humblebundle import logger


def callback(func):
    """
    A decorator to add a keyword arg 'callback' to execute a method on the return value of a function

    Used to add callbacks to the API calls

    :param func: The function to decorate
    :return: The wrapped function
    """

    def wrap(*args, **kwargs):
        callback_ = kwargs.pop('callback', None)
        result = func(*args, **kwargs)
        if callback_:
            callback_(result)
        return result

    return wrap


def deprecated(func):
    """
    A decorator which can be used to mark functions as deprecated. It will result in a warning being emitted
    to the module level logger when the function is used.
    :param func: The deprecated function
    :return: The wrapped function
    """

    def wrap(*args, **kwargs):
        logger.warn("Call to deprecated function {}.".format(func.__name__))
        return func(*args, **kwargs)

    return wrap