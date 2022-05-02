import pytest as pt
import fhirdrill as fd


# @pt.mark.reqdocker
@pt.mark.parametrize("input", ["Frame", ["Patient/1"], "Reference", "Resource"])
def test_gatherText(input, drillEnv, patientFrame, patientReference, patientResource):

    expected = [
        "S99942380",
        "M",
        "X45815551X",
        "Medical Record Number",
        "Social Security Number",
        "999-22-1962",
        "Not Hispanic or Latino",
        "White",
        "Passport Number",
        "English",
        "Aiko Jacobs",
        "e925b0f3-8006-43f6-aa31-94bd215e55e7",
        "Driver's License",
        "555-978-4581",
    ]
    d = drillEnv
    result = None
    if input == "Frame":
        result = patientFrame[:1].gatherText().data[0]
    elif input == "Reference":
        patientReference.client = d.client
        input = [patientReference]
    elif input == "Resource":
        input = [patientResource]

    if not input == "Frame":
        result = d.gatherText(input).data[0]

    assert set(result) == set(expected)
