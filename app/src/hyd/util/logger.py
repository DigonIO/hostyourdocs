"""
Module creating a basic logger setup with our preferred configuration style for the hyd package.

Author: Jendrik A. Potyka, Fabian A. Preiss.
"""
import logging
from logging import Handler, Logger, LoggerAdapter, StreamHandler, getLogger
from typing import TYPE_CHECKING

# Necessary until python3.11 (https://github.com/python/typeshed/issues/7855)
# in future just use LoggerAdapter[Logger]
if TYPE_CHECKING:
    _LoggerAdapter = LoggerAdapter[Logger]
else:
    _LoggerAdapter = LoggerAdapter


class HydLogger(_LoggerAdapter):
    """
    Custom logger wrapping around the logging.Logger class.

    Parameters
    ----------
    class_name : str
        Instance of the class the logger will be used inside of
    level : int
        loglevel where `FATAL = 50, ERROR = 40, WARNING = 30,
        INFO = 20, DEBUG = 10, NOTSET = 0`

    Notes
    -----
    It is recommended to declare a separate logger object for every class using logging.
    Using the directive ``HydLogger(type(self).__name__, level)`` inside of the ``__init__``
    function and running the ``super().__init__(level)`` from a child of said class provides
    a separate logger instance for each class as intended. Given the following definitions:

    >>> class Parent:
    ...     def __init__(self, level: Optional[int] = logging.INFO):
    ...         self.__log = HydLogger(type(self).__name__, level)
    ...
    ...     @property
    ...     def log(self):
    ...         return self.__log
    ...
    >>> class Child(Parent):
    ...     def __init__(self, level: Optional[int] = logging.INFO):
    ...         super().__init__(level)
    ...
    >>> def main():
    ...     parent = Parent()
    ...     parent.log.info("foo")
    ...     parent.log.warning("bar")
    ...
    ...     child = Child(logging.WARNING)
    ...     child.log.warning("foo")

    Finally

    >>> main()

    Generates an output similar to:

    ::

        [2021-04-20 14:18:48][INFO][Parent][main] foo
        [2021-04-20 14:18:48][WARNING][Parent][main] bar
        [2021-04-20 14:18:48][WARNING][Child][main] foo
    """

    def __init__(self, class_name: str = "Script", level: int = logging.INFO):

        self.logger: Logger = getLogger(class_name)
        handlers: list[Handler] = self.logger.handlers
        self.__console_handler: Handler

        if not handlers:
            self.logger.setLevel(logging.DEBUG)

            log_format = (
                "[%(asctime)s][%(levelname)s][%(name)s][%(funcName)s] %(message)s"
            )
            log_formatter = logging.Formatter(
                log_format,
                "%Y-%m-%d %H:%M:%S",
            )

            self.__console_handler = StreamHandler()
            self.__console_handler.setFormatter(log_formatter)
            self.__console_handler.setLevel(level)
            self.logger.addHandler(self.__console_handler)
        else:
            self.__console_handler = handlers[0]

    def setLevel(self, level: int | str = logging.INFO) -> None:
        self.__console_handler.setLevel(level)

    def process(self, msg, kwargs):
        return msg, kwargs
