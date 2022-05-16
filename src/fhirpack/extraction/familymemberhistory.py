import json
from typing import Union

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference
import fhirpack.utils as utils

import fhirpack.extraction.base as base


class ExtractorFamilyMemberHistoryMixin(base.BaseExtractorMixin):
    def getFamilyMemberHistories(
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
            input = self.castOperand(input, SyncFHIRReference, "FamilyMemberHistory")
            result = self.getResources(
                input, resourceType="FamilyMemberHistory", raw=True
            )

        elif self.isFrame and not ignoreFrame:

            utils.validateFrame(self)

            if self.resourceTypeIs("Patient"):
                input = self.data

                result = input.apply(
                    lambda x: self.searchResources(
                        # TODO allow parametrizable join parameter matrix
                        # for example, in this case patient is unsupported by the server
                        # so _content is used
                        searchParams=dict(searchParams, **{"_content": x.id}),
                        resourceType="FamilyMemberHistory",
                        raw=True,
                    )
                )
                result = result.values

            elif self.resourceTypeIs("FamilyMemberHistory"):
                input = self.data.values
                result = self.getResources(
                    input, resourceType="FamilyMemberHistory", raw=True
                )

            else:
                raise NotImplementedError

        elif searchActive:
            result = self.searchResources(
                searchParams=searchParams, resourceType="FamilyMemberHistory", raw=True
            )

        else:
            raise NotImplementedError

        result = self.prepareOutput(result, "FamilyMemberHistory")

        return result
