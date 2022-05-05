from enum import Enum


class BaseError(Exception):
    pass


class SampleError(BaseError):
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


class InvalidOperationException:
    """Raised when operation is invalid for data."""

    pass


class InvalidConfigurationException:

    pass
