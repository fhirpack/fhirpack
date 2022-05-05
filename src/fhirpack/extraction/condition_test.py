import pytest as pt
import fhirpack as fp
import tests as ts

# TODO test with resource and reference input


@pt.mark.reqdocker
@pt.mark.parametrize("input", [["5"], ["Condition/5"]])
def test_getConditions_input(input, packDocker):

    d = packDocker
    c = d.getConditions(input).data[0]

    checks = {
        "id": c["id"] == "5",
        "display": c["code"]["coding"][0]["display"]
        == "Body mass index 30+ - obesity (finding)",
        "recordedDate": c["recordedDate"] == "1989-08-05T19:37:54-04:00",
    }

    assert all(checks.values())


@pt.mark.reqdocker
@pt.mark.parametrize("searchParamsId", ["5"])
def test_getConditions_searchParams(searchParamsId, packDocker):

    d = packDocker
    searchParams = {"_id": searchParamsId}
    c = d.getConditions(searchParams=searchParams).data[0]

    checks = {
        "id": c["id"] == "5",
        "display": c["code"]["coding"][0]["display"]
        == "Body mass index 30+ - obesity (finding)",
        "recordedDate": c["recordedDate"] == "1989-08-05T19:37:54-04:00",
    }

    assert all(checks.values())


# TODO test getConditions() on Frame
