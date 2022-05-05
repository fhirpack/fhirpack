from functools import wraps
import fhirpack.exceptions as exceptions


def validateFrame(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        frame = func(*args, **kwargs)
        if frame.isnull().values.any():
            raise exceptions.InvalidInputDataException(
                "Frame must not contain null values."
            )
        if not "data" in frame.columns:
            raise exceptions.InvalidInputDataException(
                "Frame must contain a 'data' column"
            )
        return frame
    return wrapper
