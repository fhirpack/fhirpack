from typing import Union


from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference
import fhirpack.utils as utils

import fhirpack.extraction.base as base


class ExtractorDiagnosticReportMixin(base.BaseExtractorMixin):
    def getDiagnosticReports(self, *args, **kwargs):
        """Retrieves FHIR DiagnosticReport resources.

        Returns:
            Frame: Frame object storing the DiagnosticReports.
        """

        return self.getResources(*args, resourceType="DiagnosticReport", **kwargs)
