import json
from typing import Union

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference
import fhirpack.utils as utils

import fhirpack.extraction.base as base


class ExtractorMedicationMixin(base.BaseExtractorMixin):
    def getMedications(self, *args, **kwargs):
        """Retrieves FHIR Medication resources.

        Returns:
            Frame: Frame object storing the Medications.
        """

        return self.getResources(*args, resourceType="Medication", **kwargs)
