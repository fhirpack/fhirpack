from typing import Union
from tqdm import tqdm
from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference
import fhirpack.utils as utils
import fhirpack.extraction.base as base


class ExtractorConditionMixin(base.BaseExtractorMixin):
    def getConditions(
        self,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            # list[SyncFHIRResource],
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
            input = self.castOperand(input, SyncFHIRReference, "Condition")
            result = self.getResources(input, resourceType="Condition", raw=True)

        elif self.isFrame and not ignoreFrame:

            utils.validateFrame(self)

            if self.resourceTypeIs("Patient"):
                input = self.data

                result = input.apply(
                    lambda x: self.searchResources(
                        searchParams=dict(searchParams, **{"subject": x.id}),
                        resourceType="Condition",
                        raw=True,
                    )
                )
                result = result.values

            elif self.resourceTypeIs("Condition"):
                input = self.data.values
                result = self.getResources(input, resourceType="Condition", raw=True)

            else:
                raise NotImplementedError

        elif searchActive:
            result = self.searchResources(
                searchParams=searchParams, resourceType="Condition", raw=True
            )

        else:
            raise NotImplementedError

        result = self.prepareOutput(result, "Condition")

        return result
