from typing import Union


from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference
import fhirpack.utils as utils

import fhirpack.extraction.base as base


class ExtractorDocumentReferenceMixin(base.BaseExtractorMixin):
<<<<<<< HEAD
    def getDocumentReference(self, *args, **kwargs):
        """Retrieves FHIR DcoumentReference resources.

        Returns:
            Frame: Frame object storing the DocumentReferences.
        """

=======
    def getDocumentReferences(self, *args, **kwargs):
>>>>>>> main

        return self.getResources(*args, resourceType="DocumentReference", **kwargs)
