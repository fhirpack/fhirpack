import json
import importlib
from typing import Union

import pandas as pd

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference
import fhirpack.utils as utils

import fhirpack.extraction.base as base
import fhirpack.utils as utils


class ExtractorEndpointMixin(base.BaseExtractorMixin):
    def getEndpoints(
        self,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        searchParams: dict = None,
        params: dict = None,
        ignoreFrame: bool = False,
    ):
        searchActive = False if searchParams is None else True
        searchParams = {} if searchParams is None else searchParams
        params = {} if params is None else params
        input = [] if input is None else input
        result = []

        if len(input):
            raise NotImplementedError

        elif self.isFrame and not ignoreFrame:

            utils.validateFrame(self)

            if self.resourceTypeIs("ImagingStudy"):
                input = self.data
                input = self.castOperand(input, SyncFHIRReference, "Endpoint")
                result = self.getResources(input, resourceType="Endpoint", raw=True)
                result = result

            else:
                raise NotImplementedError

        elif searchActive:
            raise NotImplementedError

        else:
            raise NotImplementedError

        result = self.prepareOutput(result)

        return result
