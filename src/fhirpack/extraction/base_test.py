import pytest as pt
import tests as ts


# test getReferences after migration


@pt.fixture(scope="function")
def y(request):
    return request.param * 2


@pt.mark.reqdocker
@pt.mark.parametrize("input", [["Patient/1"], "Reference", "Resource"])
def test_getResources_onlyInput(input, packDocker, patientReference, patientResource):

    d = packDocker
    if input == "Reference":
        patientReference.client = d.client
        input = [patientReference]
    elif input == "Resource":
        input = [patientResource]
    p = d.getResources(input).data[0]

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


# TODO test_getResources_onlyFrame()


@pt.mark.reqdocker
@pt.mark.parametrize("searchParamsId", ["1"])
def test_searchResources_patientId(searchParamsId, packDocker):

    d = packDocker
    input = {"searchParams": {"_id": searchParamsId}, "resourceType": "Patient"}
    p = d.searchResources(**input).data[0]

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


# TODO test searchResources() with raw=True


@pt.mark.reqdocker
def test_getFromFiles_singleResource(packDocker):

    d = packDocker
    dataPath = f"{ts.TEST_DATA_DIR}/fhirpack.extraction.base.getFromFiles.patient.00.in"
    p = d.getFromFiles([dataPath]).data[0]

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


def test_getFromFiles_multipleResourcesFromOneFile(packUnconnected):

    d = packUnconnected
    dataPath = (
        f"{ts.TEST_DATA_DIR}/fhirpack.extraction.base.getFromFiles.patients.00.in"
    )
    data = d.getFromFiles([dataPath]).data

    p1 = data[0]
    p2 = data[1]

    checks1 = {
        "pid": p1["id"] == "1",
        "pname": p1["name"]
        == [
            {
                "use": "official",
                "family": "Koepp",
                "given": ["Abdul"],
                "prefix": ["Mr."],
            }
        ],
        "pbirth": p1["birthDate"] == "1954-10-02",
    }

    checks2 = {
        "pid": p2["id"] == "181",
        "pname": p2["name"]
        == [
            {
                "use": "official",
                "family": "Hartmann",
                "given": ["Adalberto"],
                "prefix": ["Mr."],
            }
        ],
        "pbirth": p2["birthDate"] == "1948-01-28",
    }

    ok = all(checks1.values()) and all(checks2.values())

    assert ok


def test_getFromFiles_multipleResourcesMultipleFiles(packUnconnected):

    d = packUnconnected
    data = d.getFromFiles(
        [
            f"{ts.TEST_DATA_DIR}/fhirpack.extraction.base.getFromFiles.patient.00.in",
            f"{ts.TEST_DATA_DIR}/fhirpack.extraction.base.getFromFiles.patients.00.in",
        ]
    ).data

    p1 = data[0]
    p2 = data[2]

    checks1 = {
        "pid": p1["id"] == "1",
        "pname": p1["name"]
        == [
            {
                "use": "official",
                "family": "Koepp",
                "given": ["Abdul"],
                "prefix": ["Mr."],
            }
        ],
        "pbirth": p1["birthDate"] == "1954-10-02",
    }

    checks2 = {
        "pid": p2["id"] == "181",
        "pname": p2["name"]
        == [
            {
                "use": "official",
                "family": "Hartmann",
                "given": ["Adalberto"],
                "prefix": ["Mr."],
            }
        ],
        "pbirth": p2["birthDate"] == "1948-01-28",
    }

    ok = all(checks1.values()) and all(checks2.values())

    assert ok


def test_getFromFiles_multipleResourcesError(packUnconnected):

    d = packUnconnected
    with pt.raises(TypeError):
        data = d.getFromFiles(
            [
                f"{ts.TEST_DATA_DIR}/fhirpack.extraction.base.getFromFiles.patients.00.in",
                f"{ts.TEST_DATA_DIR}/fhirpack.extraction.base.getFromFiles.observation.00.in",
            ]
        ).data
