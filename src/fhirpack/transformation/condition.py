import json
import importlib
from typing import Union

import pandas as pd

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference

import fhirpack.transformation.base as base


class TransformerConditionMixin(base.BaseTransformerMixin):
    def transformerConditionMethod(
        self,
    ):

        pass
