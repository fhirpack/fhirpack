__author__ = "Jayson Salazar"
__copyright__ = "Jayson Salazar"
__license__ = ""


import tests.data as td
import fhirpack as fp
import pytest as pt
import numpy as np
import pandas as pd
import tests as ts

# this is an example of a test that uses
# the fixture defined at /conftest.py with session scope

# def test_usesGlobalSessionFixture(globalSessionFixture):
#     print(globalSessionFixture)
#     assert 1 == 1


def test_keys_forPatients():

    input = td.jsonFile("fhirpack.utils.keys.forPatients.00.in")
    expected = td.jsonFile("fhirpack.utils.keys.forPatients.00.out")

    result = list(fp.utils.keys(input))

    ok = result == expected

    assert ok


def test_valuesForKeys_onlyDicts():
    """only dictionaries in input data"""

    input = td.jsonFile("fhirpack.utils.valuesForKeys.patient.00.in")

    expected = ["Boston", "Springfield"]

    result = list(fp.utils.valuesForKeys(input, ["city"]))

    ok = result == expected

    assert ok


def test_valuesForKeys_dictsAndLists():
    """only dicts in input data"""

    input = td.jsonFile("fhirpack.utils.valuesForKeys.patient.00.in")

    expected = [
        "https://smarthealthit.org/tags",
        "urn:oid:2.16.840.1.113883.6.238",
        "urn:oid:2.16.840.1.113883.6.238",
        9.195822017359179,
        18.804177982640823,
        "https://github.com/synthetichealth/synthea",
        "http://terminology.hl7.org/CodeSystem/v2-0203",
        "http://hospital.smarthealthit.org",
        "http://terminology.hl7.org/CodeSystem/v2-0203",
        "http://hl7.org/fhir/sid/us-ssn",
        "http://terminology.hl7.org/CodeSystem/v2-0203",
        "urn:oid:2.16.840.1.113883.4.3.25",
        "http://terminology.hl7.org/CodeSystem/v2-0203",
        "http://standardhealthrecord.org/fhir/StructureDefinition/passportNumber",
        "phone",
        42.115454,
        -72.539978,
        "http://terminology.hl7.org/CodeSystem/v3-MaritalStatus",
        "urn:ietf:bcp:47",
    ]

    result = list(fp.utils.valuesForKeys(input, ["system", "valueDecimal"]))

    ok = result == expected

    assert ok


def test_guessBufferMIMEType(globalSessionFixture):
    assert 1 == 1


@pt.mark.reqdocker
@pt.mark.parametrize("input", [np.nan, None, pd.NA, np.NaN])
def test_validateFrame_NullValues(input, packDocker):

    d = packDocker

    p = d.getPatients(["1"])
    nullValues = fp.base.Frame({"data": [input]})
    brokenFrame = p.append(nullValues)

    with pt.raises(fp.exceptions.InvalidInputDataException):
        fp.utils.validateFrame(brokenFrame)


def test_validateFrame_Unconnected(packUnconnected):

    d = packUnconnected
    d.client = None
    dataPath = f"{ts.TEST_DATA_DIR}/fhirpack.extraction.base.getFromFiles.patient.00.in"
    p = d.getFromFiles([dataPath]).data[0]

    with pt.raises(fp.exceptions.ServerConnectionException):
        fp.utils.validateFrame(p)
