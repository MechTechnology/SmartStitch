import functools
import logging
import os
from datetime import datetime

from ..utils.constants import LOG_REL_DIR


class GlobalLogger:
    @classmethod
    def configureGlobalLogger(self):
        """Initializes and Configures Logging Service"""
        if not os.path.exists(LOG_REL_DIR):
            os.makedirs(LOG_REL_DIR)
        current_date = datetime.now()
        log_filename = current_date.strftime('log-%Y-%m-%d.log')
        log_filename = os.path.join(LOG_REL_DIR, log_filename)

        log_level = logging.DEBUG
        log_format = '%(levelname)s:%(asctime)s:%(message)s'
        logging.basicConfig(format=log_format, filename=log_filename, level=log_level)
        logging.debug('GlobalLogger:Logger Initialized')
        # Removes the pil logging from polluting the Debug Level.
        pil_logger = logging.getLogger('PIL')
        pil_logger.setLevel(logging.INFO)

    @classmethod
    def log_warning(self, message, caller='GlobalLogger', *args, **kwargs):
        log_msg = f'{caller}:{message}'
        logging.warning(log_msg, *args, **kwargs)

    @classmethod
    def log_debug(self, message, caller='GlobalLogger', *args, **kwargs):
        log = f'{caller}:{message}'
        logging.debug(log, *args, **kwargs)


def logFunc(func=None, inclass=False):
    if func is None:
        return functools.partial(logFunc, inclass=inclass)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        caller_class = "GlobalLogger"
        args_repr = [repr(a) for a in args]
        if inclass:
            caller_class = type(args[0]).__name__
            args_repr = [repr(args[i]) for i in range(1, len(args))]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        GlobalLogger.log_debug(f'{func.__name__}:args:{signature}', caller_class)
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logging.exception(
                f"Exception raised in {func.__name__}. exception: {str(e)}"
            )
            raise e

    return wrapper


GlobalLogger.configureGlobalLogger()
