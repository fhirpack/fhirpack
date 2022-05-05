import importlib
from typing import Union

import pandas as pd

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference

import fhirpack.load.base as base


class LoaderObservationMixin(base.BaseLoaderMixin):
    def transformerObservationMethod(
        self,
    ):
        pass
