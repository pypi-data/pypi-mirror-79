import logging
import abc
import six

from pathlib import Path


@six.add_metaclass(abc.ABCMeta)
class OutputHandler:
    """
    Base class for handling the output of the CLI application.
    """

    @abc.abstractmethod
    def handle(self, output: str):
        """
        Method to be overridden by subclasses to perform the action on the output
        """


class ConsoleHandler(OutputHandler):
    """
    OutputHandler that logs the output to the console via loggers
    """

    def __init__(self, logger_name: str):
        self.logger = logging.getLogger(logger_name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Loggers do not need to be closed
        pass

    def handle(self, output: str):
        self.logger.info(output)


class FileHandler(OutputHandler):
    """
    OutputHandler that logs the output to a specified file
    """

    def __init__(self, file: str):
        self.file = open(Path(file), "w")

    def __enter__(self):
        return self

    def __exit__(self, type, val, traceback):
        self.file.close()

    def handle(self, output: str):
        self.file.write(output + "\n")
