import functools
import logging
import os
from datetime import datetime

from ..utils.constants import LOG_REL_DIR

# GlobalLogger class to handle logging configuration and messages
class GlobalLogger:
    @classmethod
    def configureGlobalLogger(self):
        """Initializes and Configures Logging Service"""
        # Create log directory if it doesn't exist
        if not os.path.exists(LOG_REL_DIR):
            os.makedirs(LOG_REL_DIR)
        
        # Generate log file name based on the current date
        current_date = datetime.now()
        log_filename = current_date.strftime('log-%Y-%m-%d.log')
        log_filename = os.path.join(LOG_REL_DIR, log_filename)
        
        # Set logging level to DEBUG and define the log message format
        log_level = logging.DEBUG
        log_format = '%(levelname)s:%(asctime)s:%(message)s'
        logging.basicConfig(format=log_format, filename=log_filename, level=log_level)
        
        # Log that the logger has been initialized
        logging.debug('GlobalLogger:Logger Initialized')
        
        # Remove the PIL (Python Imaging Library) logging from polluting the Debug Level
        pil_logger = logging.getLogger('PIL')
        pil_logger.setLevel(logging.INFO)

    @classmethod
    def log_warning(self, message, caller='GlobalLogger', *args, **kwargs):
        # Log a warning message with the provided message and caller information
        log_msg = f'{caller}:{message}'
        logging.warning(log_msg, *args, **kwargs)

    @classmethod
    def log_debug(self, message, caller='GlobalLogger', *args, **kwargs):
        # Log a debug message with the provided message and caller information
        log = f'{caller}:{message}'
        logging.debug(log, *args, **kwargs)

# Decorator function to log function calls
def logFunc(func=None, inclass=False):
    if func is None:
        return functools.partial(logFunc, inclass=inclass)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Determine the caller class and format the function signature with its arguments
        caller_class = "GlobalLogger"
        args_repr = [repr(a) for a in args]
        if inclass:
            caller_class = type(args[0]).__name__
            args_repr = [repr(args[i]) for i in range(1, len(args))]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        
        # Log the function call with its arguments and caller information
        GlobalLogger.log_debug(f'{func.__name__}:args:{signature}', caller_class)
        
        try:
            # Call the original function and return its result
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            # Log and re-raise any exceptions that occur during the function call
            logging.exception(
                f"Exception raised in {func.__name__}. exception: {str(e)}"
            )
            raise e

    return wrapper

# Configure the GlobalLogger when this script is executed
GlobalLogger.configureGlobalLogger()