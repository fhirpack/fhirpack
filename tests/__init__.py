import os
import inspect
import pathlib

import fhirpack

PACKAGE_INSTALLATION_DIR = os.path.dirname(fhirpack.__file__)

CURRENT_DIR = pathlib.Path().resolve()
TEST_DATA_DIR = f"{CURRENT_DIR}/tests/data"


DEBUG = True
# DEBUG=False

__INITIAL_DEBUG_OUTPUT = {
    "INSTALLATION DIRECTORY": PACKAGE_INSTALLATION_DIR,
    # "":,
}


def debug(message):
    if not DEBUG:
        return

    print("\n")
    print(
        f"[DEBUG] {os.path.basename(inspect.stack()[1][1])} {inspect.stack()[1][3]}()"
    )
    print(f"[MESSAGE] {message}")


debug("tests/__init__.py general debug information")

for k, v in __INITIAL_DEBUG_OUTPUT.items():
    debug(f"{k}: {v}")
