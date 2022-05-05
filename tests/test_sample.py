__author__ = "Jayson Salazar"
__copyright__ = "Jayson Salazar"
__license__ = ""

import pytest as pt
import tests as ts
import fhirpack as fp
import fhirpy


# this is an example fixture with module scope,
# for the tests package, with autouse enabled and a finalizer

# @pytest.fixture(scope="module",autouse=True)
# def testsModuleFixture(request):
#   tests.debug("tests module confSetup")

#   def testsModuleFixtureFin():
#     tests.debug('tests module confTeardown')
#     pass
#   request.addfinalizer(testsModuleFixtureFin)


print("[debug pytest] INSTALLATION DIRECTORY: ", ts.PACKAGE_INSTALLATION_DIR)


@pt.mark.reqdocker
def test_sample(packDocker):

    d = packDocker
    ts.debug(d.client)
    p = d.getPatients(["Patient/1"]).data[0]

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
