import json
import importlib
from typing import Union

import pandas as pd

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference

import fhirdrill.transformation.base as base


class TransformerObservationMixin(base.BaseTransformerMixin):
    def transformerObservationMethod(
        self,
    ):
        pass
