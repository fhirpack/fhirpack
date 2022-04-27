import json
import importlib
from typing import Union

import pandas as pd

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference

import fhirdrill.load.base as base


class LoaderConditionMixin(base.BaseLoaderMixin):
    def transformerConditionMethod(
        self,
    ):

        pass
