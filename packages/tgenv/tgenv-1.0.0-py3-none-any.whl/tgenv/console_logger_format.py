import logging
from logging import Formatter

class ConsoleLoggingFormat(Formatter):
    """ A logging format for stdout
    """

    STANDARD_FORMAT = "%(message)s"
    ERROR_FORMAT = "\033[0;31m%(message)s\033[0m"
    WARNING_FORMAT = "\033[1;33m%(message)s\033[0m"

    def __init__(self):
        Formatter.__init__(self, fmt="\t%(msg)s", style='%')

    # pylint: disable=protected-access
    def format(self, record):
        """ Overrides the default format
        """
        org_fmt = self._style._fmt

        if record.levelno == logging.DEBUG:
            self._style._fmt = ConsoleLoggingFormat.STANDARD_FORMAT

        elif record.levelno == logging.INFO:
            self._style._fmt = ConsoleLoggingFormat.STANDARD_FORMAT

        elif record.levelno == logging.ERROR:
            self._style._fmt = ConsoleLoggingFormat.ERROR_FORMAT

        elif record.levelno == logging.WARNING:
            self._style._fmt = ConsoleLoggingFormat.WARNING_FORMAT

        self._style._fmt = org_fmt

        return logging.Formatter.format(self, record)
    # pylint: enable=protected-access
