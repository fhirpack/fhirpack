import pytest as pt
import tests as ts
import fhirpack as fp

# this is an example fixture with session scope,
# for the tests package, with autouse enabled and a finalizer
# this fixture can be used by any test under tests/


@pt.fixture(scope="session", autouse=True)
def testsSessionFixture(request):
    ts.debug("tests session confSetup")

    def testsSessionFixtureFin():
        ts.debug("tests session confTeardown")
        pass

    request.addfinalizer(testsSessionFixtureFin)
