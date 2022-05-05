import json
import importlib
from typing import Union

import pandas as pd

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference

import fhirpack.load.base as base


class LoaderConditionMixin(base.BaseLoaderMixin):
    def transformerConditionMethod(
        self,
    ):

        pass
