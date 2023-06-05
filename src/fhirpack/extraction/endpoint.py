import json
import importlib
from typing import Union

import pandas as pd

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference
import fhirpack.utils as utils

import fhirpack.extraction.base as base
import fhirpack.utils as utils


class ExtractorEndpointMixin(base.BaseExtractorMixin):
    def getEndpoints(self, *args, **kwargs):
        """Retrieves FHIR Endpoint resources.

        Returns:
            Frame: Frame object storing the Endpoints.
        """

        return self.getResources(*args, resourceType="Endpoint", **kwargs)
