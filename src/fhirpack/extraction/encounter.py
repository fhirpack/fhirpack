import json
from typing import Union

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference
import fhirpack.utils as utils

import fhirpack.extraction.base as base


class ExtractorEncounterMixin(base.BaseExtractorMixin):
    def getEncounters(self, *args, **kwargs):
        """Retrieves FHIR Encounter resources.

        Returns:
            Frame: Frame object storing the Encounters.
        """

        return self.getResources(*args, resourceType="Encounter", **kwargs)
