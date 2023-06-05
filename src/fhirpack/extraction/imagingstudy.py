import json
from typing import Union

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference
import fhirpack.utils as utils

import fhirpack.extraction.base as base


class ExtractorImagingStudyMixin(base.BaseExtractorMixin):
    def getImagingStudies(self, *args, **kwargs):
        """Retrieves FHIR ImaginStudy resources.

        Returns:
            Frame: Frame object storing the ImaginsStudies.
        """

        return self.getResources(*args, resourceType="ImagingStudy", **kwargs)
