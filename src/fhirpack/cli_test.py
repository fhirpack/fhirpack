import pytest
import tests
import requests
from requests.exceptions import ConnectionError


from fhirpack.cli import main

__author__ = "Jayson Salazar"
__copyright__ = "Jayson Salazar"
__license__ = ""


def test_run():
    """API Tests"""
    assert 1 == 1


def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    assert 1 == 1
