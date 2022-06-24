from typing import Union
from tqdm import tqdm
from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference
import fhirpack.utils as utils
import fhirpack.extraction.base as base


class ExtractorConditionMixin(base.BaseExtractorMixin):
    def getConditions(self, *args, **kwargs):

        return self.getResources(*args, resourceType="Condition", **kwargs)
