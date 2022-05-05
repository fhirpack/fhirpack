__author__ = "Jayson Salazar"
__copyright__ = "Jayson Salazar"
__license__ = ""


import json

import pytest
import tests

from fhirpack.pack import PACK


def textFile(file):
    with open(f"{tests.TEST_DATA_DIR}/{file}", "r") as f:
        data = f.readlines()
        return "\n".join(data)


def jsonFile(file):
    return json.loads(textFile(file))
