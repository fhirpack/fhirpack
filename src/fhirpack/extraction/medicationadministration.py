import json
from typing import Union

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference
import fhirpack.utils as utils

import fhirpack.extraction.base as base


class ExtractorMedicationAdministrationMixin(base.BaseExtractorMixin):
    def getMedicationAdministrations(self, *args, **kwargs):

        return self.getResources(
            *args, resourceType="MedicationAdministration", **kwargs
        )
