import json
from typing import Union

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference
import fhirpack.utils as utils

import fhirpack.extraction.base as base


class ExtractorFamilyMemberHistoryMixin(base.BaseExtractorMixin):
    def getFamilyMemberHistories(self, *args, **kwargs):
        """Retrieves FHIR FamilyMemberHistory resources.

        Returns:
            Frame: Frame object storing the FamilyMemberHistories.
        """

        return self.getResources(*args, resourceType="FamilyMemberHistory", **kwargs)
