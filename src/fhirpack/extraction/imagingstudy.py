import fhirpack.extraction.base as base
import json
from typing import Union
import math

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference
import fhirpack.utils as utils

import numpy as np
from tqdm import tqdm

tqdm.pandas()


class ExtractorImagingStudyMixin(base.BaseExtractorMixin):
    def getImagingStudies(
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
            input = self.castOperand(input, SyncFHIRReference, "ImagingStudy")
            result = self.getResources(input, resourceType="ImagingStudy", raw=True)

        elif self.isFrame and not ignoreFrame:

            utils.validateFrame(self)

            if self.resourceTypeIs("Patient"):
                input = self.data

                result = input.apply(
                    lambda x: self.searchResources(
                        searchParams=dict(searchParams, **{"subject": x.id}),
                        resourceType="ImagingStudy",
                        raw=True,
                    )
                )
                result = result.values

            elif self.resourceTypeIs("ImagingStudy"):
                raise NotImplementedError

            else:
                raise NotImplementedError

        elif searchActive:
            result = self.searchResources(
                searchParams=searchParams, resourceType="ImagingStudy", raw=True
            )

        else:
            raise NotImplementedError

        result = self.prepareOutput(result, "ImagingStudy")

        return result
