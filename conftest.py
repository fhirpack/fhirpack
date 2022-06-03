"""
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import fhirpy
import fhirpack as fp
import tests as ts
import pytest as pt
import requests
from pathlib import Path
import os
import re

pytest_plugins = ["docker_compose"]


# this is an example fixture with session scope,
# for all packages, with autouse enabled and a finalizer
# this fixture can be used by any test in the repository


@pt.fixture(scope="session", autouse=True)
def globalSessionFixture(request):

    ts.debug("global session confSetup")

    def globalSessionFixtureFin():
        ts.debug("global session confTeardown")
        pass

    request.addfinalizer(globalSessionFixtureFin)


@pt.fixture(scope="session")
def fhirServerDocker(session_scoped_container_getter):
    """Wait for the api from my_api_service to become responsive"""

    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    session.mount("http://", HTTPAdapter(max_retries=retries))

    service = session_scoped_container_getter.get("r4").network_info[0]
    api_url = "http://%s:%s/" % (service.hostname, service.host_port)
    assert session.get(api_url)
    return session, api_url


@pt.fixture(scope="session")
def packUnconnected(request):

    ts.debug("global session pack")
    # session, apiUrl = remoteFhirServer
    # client = fhirpy.SyncFHIRClient(f"{apiUrl}hapi-fhir-jpaserver/fhir")

    def globalSessionFixtureFin():
        ts.debug("global session pack Teardown")
        pass

    request.addfinalizer(globalSessionFixtureFin)

    # pack = fp.PACK(unconnected=True)
    pack = fp.PACK("")
    return pack


@pt.fixture(scope="session")
def packEnv(request):

    ts.debug("global session pack")
    # session, apiUrl = remoteFhirServer
    # client = fhirpy.SyncFHIRClient(f"{apiUrl}hapi-fhir-jpaserver/fhir")

    def globalSessionFixtureFin():
        ts.debug("global session pack Teardown")
        pass

    request.addfinalizer(globalSessionFixtureFin)

    pack = fp.PACK(envFile=".env.example")
    return pack


@pt.fixture(scope="session")
def packDocker(request, fhirServerDocker):
    ts.debug("global session localPACK")

    session, apiUrl = fhirServerDocker

    def globalSessionFixtureFin():
        ts.debug("global session confTeardown")
        pass

    request.addfinalizer(globalSessionFixtureFin)

    return fp.PACK(f"{apiUrl}hapi-fhir-jpaserver/fhir")


@pt.fixture(scope="function")
def functionData(request):

    # behaves differently on linux and mac, src. prepended on mac
    # moduleName = request.module.__name__

    installationPath = os.path.dirname(fp.__file__)
    installationPath = str(Path(installationPath).parent.absolute())

    testSessionPath = str(request.session.path)
    # /home/jsalazar/git/projects/lib-fhirpack

    testPath = str(request.fspath)
    # /home/jsalazar/git/projects/lib-fhirpack/src/fhirpack/utils_test.p

    testPath = testPath.split(f"{installationPath}/")
    # ['', '/src/fhirpack/utils_test.py']

    if len(testPath) == 1:
        testPath = testPath[0].split(testSessionPath)

    testRelativePath = (
        testPath[1]
        .replace("src/", "")
        .replace("/", ".")
        .replace("_test", "")
        .replace("test_", "")
        .replace(".py", "")
    )  # fhirpack.utils
    # tests.cli

    testedFunctionName = request.function.__name__
    testedFunctionName = testedFunctionName.split("_")[1]
    # valuesForKeys
    # run
    # main
    # guessBufferMIMEType

    if testRelativePath:
        libraryDataPrefix = f"all"
        packageDataPrefix = f"fhirpack"

        functionDataPrefix = f"{testRelativePath}.{testedFunctionName}"
        # tests.cli.main
        # fhirpack.utils.guessBufferMIMEType
        # fhirpack.utils.valuesForKeys
    else:
        packageDataPrefix = f"tests"

    testDataFiles = []

    # pt.set_trace()

    availableDataFiles = sorted(os.listdir(ts.TEST_DATA_DIR))

    for f in availableDataFiles:
        if re.match(f"{functionDataPrefix}.[a-zA-Z]+.[0-9]+..?", f):
            testDataFiles.append(f)
        elif re.match(f"{packageDataPrefix}.[a-zA-Z]+.[0-9]+..?", f):
            testDataFiles.append(f)
        elif re.match(f"{libraryDataPrefix}.[a-zA-Z]+.[0-9]+..?", f):
            testDataFiles.append(f)

    data = testDataFiles

    indata = [e for e in data if ".in" in e]
    outdata = [e for e in data if ".out" in e]

    return {"in": indata, "out": outdata}
