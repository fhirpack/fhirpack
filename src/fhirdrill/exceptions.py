import json
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
