import json
from typing import Union

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference
import fhirpack.utils as utils

import fhirpack.extraction.base as base


class ExtractorProcedureMixin(base.BaseExtractorMixin):
    def getProcedures(self, *args, **kwargs):
        """Retrieves FHIR Procedure resources.

        Returns:
            Frame: Frame object storing the Procedures.
        """

        return self.getResources(
            *args, resourceType="Procedure", **kwargs
        )
