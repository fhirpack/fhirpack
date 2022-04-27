import pytest as pt
import fhirdrill as fd
from fhirpy.lib import SyncFHIRResource, SyncFHIRReference
import tests as ts


def test_guessOutputResourceType_resource(drillUnconnected, patientResourceList):
    expected = "Patient"
    result = drillUnconnected.guessOutputResourceType(patientResourceList)
    ok = expected == result
    assert ok


def test_guessOutputResourceType_reference(drillUnconnected, patientReferenceList):
    expected = "Patient"
    result = drillUnconnected.guessOutputResourceType(patientReferenceList)
    ok = expected == result
    assert ok


def test_guessOutputResourceType_dict(drillUnconnected, patientAsDict):
    """Testing with dictionary input, the dict got to have the resourceTpye key"""

    input = {"resourceType": "Patient"}
    expected = "Patient"
    result = drillUnconnected.guessOutputResourceType([patientAsDict])
    ok = expected == result
    assert ok


def test_guessOutputResourceType_uninitializedType(drillUnconnected):

    # other type than dic, resource or reference
    input = ["random string"]
    expected = "Uninitialized"
    result = drillUnconnected.guessOutputResourceType(input)
    ok = expected == result
    assert ok


def test_guessOutputResourceType_mixed(
    drillUnconnected, observationResourceList, patientResourceList
):

    input = [patientResourceList[0], observationResourceList[0]]
    expected = "Mixed"
    result = drillUnconnected.guessOutputResourceType(input)
    ok = expected == result
    assert ok


# # TODO: Test prepareCompositeOutput


# # TODO: Add more tests for prepareOutput


def test_prepareOutput_noResourceType(drillUnconnected, patientResourceList):

    p = drillUnconnected.prepareOutput(patientResourceList).data[0]

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


def test_parseReference_stringSlash(drillUnconnected, patientReference):

    d = drillUnconnected
    input = "Patient/1"
    expected = patientReference
    result = d.parseReference(input)
    ok = result == expected
    assert ok


# # TODO: Implement test for string without /id
def test_parseReference_stringNoSlashWithResourceType(
    drillUnconnected, patientReference
):
    d = drillUnconnected
    input = "Patient/1"
    expected = patientReference
    result = d.parseReference(input)
    ok = result == expected
    assert ok


def test_parseReference_reference(drillUnconnected, patientReference):

    d = drillUnconnected
    # .reference gives the string representation of a SyncFHIRReference
    input = patientReference.reference
    expected = patientReference
    result = d.parseReference(input)
    ok = result == expected
    assert ok


def test_prepareReferences_sinlgeReference(drillUnconnected, patientReference):

    d = drillUnconnected
    input = [patientReference]
    expected = [patientReference]
    result = d.prepareReferences(input)
    ok = result == expected
    assert ok


def test_prepareReferences_twoStrings(drillUnconnected, patientReference):

    d = drillUnconnected
    input = ["Patient/1", "Patient/1"]
    expected = [patientReference] * 2
    result = d.prepareReferences(input)
    ok = result == expected
    assert ok


# # TODO test prepareOperationInput


@pt.mark.reqdocker
def test_castOperand_stringToResource(drillDocker):

    input = {"input": ["Patient/1"], "target": SyncFHIRResource}
    expected = SyncFHIRResource
    d = drillDocker
    result = d.castOperand(**input)
    ok = isinstance(result[0], expected)
    assert ok


def test_castOperand_stringToReference(drillUnconnected):

    input = {"input": ["Patient/1"], "target": SyncFHIRReference}
    expected = SyncFHIRReference
    d = drillUnconnected
    result = d.castOperand(**input)

    ok = isinstance(result[0], expected)

    assert ok


@pt.mark.reqdocker
def test_castOperand_resourceToReference(patientResource, drillUnconnected):

    input = {"input": [patientResource], "target": SyncFHIRReference}
    expected = SyncFHIRReference
    d = drillUnconnected
    result = d.castOperand(**input)

    ok = isinstance(result[0], expected)

    assert ok


@pt.mark.reqdocker
def test_castOperand_referenceToResource(patientReference, drillDocker):

    input = {"input": [patientReference.reference], "target": SyncFHIRResource}
    expected = SyncFHIRResource
    d = drillDocker
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
