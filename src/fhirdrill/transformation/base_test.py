import pytest as pt
import fhirdrill as fd

@pt.mark.reqdocker
@pt.mark.parametrize("input", ["Frame", ["Patient/1"], "Reference", "Resource"])
def test_gatherText(input, drillDocker, patientFrame, patientReference, patientResource):

    expected = [
        "White",
        "White",
        "Not Hispanic or Latino",
        "Not Hispanic or Latino",
        "Aiko Jacobs",
        "Medical Record Number",
        "Medical Record Number",
        "Social Security Number",
        "Social Security Number",
        "Driver's License",
        "Driver's License",
        "Passport Number",
        "Passport Number",
        "M",
        "M",
        "English",
        "English",
    ]

    d = drillDocker
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

    assert result == expected