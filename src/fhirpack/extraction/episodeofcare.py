from typing import Union

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference
import fhirpack.utils as utils

import fhirpack.extraction.base as base


class ExtractorEpisodeOfCareMixin(base.BaseExtractorMixin):
    def getEpisodesOfCare(self, *args, **kwargs):
        """Retrieves FHIR EpisodeOfCare resources.

        Returns:
            Frame: Frame object storing the EpisodeOfCares.
        """

        return self.getResources(*args, resourceType="EpisodeOfCare", **kwargs)
