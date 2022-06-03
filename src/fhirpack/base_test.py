import pytest as pt

from fhirpy.lib import SyncFHIRResource, SyncFHIRReference

import tests as ts
import fhirpack as fp


def test_guessOutputResourceType_resource(packUnconnected, patientResourceList):
    expected = "Patient"
    result = packUnconnected.guessOutputResourceType(patientResourceList)
    ok = expected == result
    assert ok


def test_guessOutputResourceType_reference(packUnconnected, patientReferenceList):
    expected = "Patient"
    result = packUnconnected.guessOutputResourceType(patientReferenceList)
    ok = expected == result
    assert ok


def test_guessOutputResourceType_dict(packUnconnected, patientAsDict):
    """Testing with dictionary input, the dict got to have the resourceTpye key"""

    input = {"resourceType": "Patient"}
    expected = "Patient"
    result = packUnconnected.guessOutputResourceType([patientAsDict])
    ok = expected == result
    assert ok


def test_guessOutputResourceType_uninitializedType(packUnconnected):

    # other type than dic, resource or reference
    input = ["random string"]
    expected = "Uninitialized"
    result = packUnconnected.guessOutputResourceType(input)
    ok = expected == result
    assert ok


def test_guessOutputResourceType_mixed(
    packUnconnected, observationResourceList, patientResourceList
):

    input = [patientResourceList[0], observationResourceList[0]]
    expected = "Mixed"
    result = packUnconnected.guessOutputResourceType(input)
    ok = expected == result
    assert ok


# # TODO: Test prepareCompositeOutput


# # TODO: Add more tests for prepareOutput


def test_prepareOutput_noResourceType(packUnconnected, patientResourceList):

    p = packUnconnected.prepareOutput(patientResourceList).data[0]

    checks = {
        "pid": p["id"] == "1",
        "pname": p["name"]
        == [
            {
                "use": "official",
                "family": "Koepp",
                "given": ["Abdul"],
                "prefix": ["Mr."],
            }
        ],
        "pbirth": p["birthDate"] == "1954-10-02",
    }

    assert all(checks.values())


def test_parseReference_stringSlash(packUnconnected, patientReference):

    d = packUnconnected
    input = "Patient/1"
    expected = patientReference
    result = d.parseReference(input)
    ok = result == expected
    assert ok


# # TODO: Implement test for string without /id
def test_parseReference_stringNoSlashWithResourceType(
    packUnconnected, patientReference
):
    d = packUnconnected
    input = "Patient/1"
    expected = patientReference
    result = d.parseReference(input)
    ok = result == expected
    assert ok


def test_parseReference_reference(packUnconnected, patientReference):

    d = packUnconnected
    # .reference gives the string representation of a SyncFHIRReference
    input = patientReference.reference
    expected = patientReference
    result = d.parseReference(input)
    ok = result == expected
    assert ok


def test_prepareReferences_sinlgeReference(packUnconnected, patientReference):

    d = packUnconnected
    input = [patientReference]
    expected = [patientReference]
    result = d.prepareReferences(input)
    ok = result == expected
    assert ok


def test_prepareReferences_twoStrings(packUnconnected, patientReference):

    d = packUnconnected
    input = ["Patient/1", "Patient/1"]
    expected = [patientReference] * 2
    result = d.prepareReferences(input)
    ok = result == expected
    assert ok


# # TODO test prepareOperationInput


@pt.mark.reqdocker
def test_castOperand_stringToResource(packDocker):

    input = {"input": ["Patient/1"], "target": SyncFHIRResource}
    expected = SyncFHIRResource
    d = packDocker
    result = d.castOperand(**input)
    ok = isinstance(result[0], expected)
    assert ok


def test_castOperand_stringToReference(packUnconnected):

    input = {"input": ["Patient/1"], "target": SyncFHIRReference}
    expected = SyncFHIRReference
    d = packUnconnected
    result = d.castOperand(**input)

    ok = isinstance(result[0], expected)

    assert ok


@pt.mark.reqdocker
def test_castOperand_resourceToReference(patientResource, packUnconnected):

    input = {"input": [patientResource], "target": SyncFHIRReference}
    expected = SyncFHIRReference
    d = packUnconnected
    result = d.castOperand(**input)

    ok = isinstance(result[0], expected)

    assert ok


@pt.mark.reqdocker
def test_castOperand_referenceToResource(patientReference, packDocker):

    input = {"input": [patientReference.reference], "target": SyncFHIRResource}
    expected = SyncFHIRResource
    d = packDocker
    result = d.castOperand(**input)

    ok = isinstance(result[0], expected)

    assert ok


def test_frame_resourceTypeIsTrue(patientFrame):

    expected = "patient"
    ok = patientFrame.resourceTypeIs(expected)

    assert ok


def test_frame_resourceTypeIsFalse(patientFrame):

    expected = "observation"
    ok = not patientFrame.resourceTypeIs(expected)

    assert ok


# TODO test Frame.explode
# TODO test Frame.keys
# TODO test Frame.explode
# TODO test Frame.print
