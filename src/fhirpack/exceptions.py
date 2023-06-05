from enum import Enum


class BaseException(Exception):
    pass


class ErrorSeverity(Enum):
    fatal = "fatal"
    error = "error"
    warning = "warning"
    information = "information"


class ServerConnectionException(ConnectionError):
    """Raised when pack does not have connection to server."""

    pass


class InvalidInputDataException(ValueError):
    """Raised when invalid input types are passed."""

    pass


class InvalidSearchParams(ValueError):
    """Raised when invalid key is used for searchParams"""

    pass


class InvalidOperationException(BaseException):
    """Raised when operation is invalid for data."""

    pass


class InvalidConfigurationException(BaseException):
    """Raised when operation is invalid for data."""

    pass
