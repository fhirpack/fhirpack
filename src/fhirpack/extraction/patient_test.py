import pytest as pt
import fhirpack as fp


# TODO test with resource and reference input
@pt.mark.reqdocker
@pt.mark.parametrize("input", [["1"], ["Patient/1"]])
def test_getPatients_input(input, packDocker):

    d = packDocker
    p = d.getPatients(input).data[0]

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


@pt.mark.reqdocker
@pt.mark.parametrize("searchParamsId", [["1"], ["Patient/1"]])
def test_getPatients_searchParams(searchParamsId, packDocker):

    d = packDocker
    searchParams = {"_id": searchParamsId}
    p = d.getPatients(searchParams=searchParams).data[0]

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

    # TODO test getPatients() on Frame
