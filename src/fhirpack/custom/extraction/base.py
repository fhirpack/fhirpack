import json
import importlib
from typing import Union

import pandas as pd

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference

# import fhirpack.utils as utils


class PluginBaseExtractorMixin:
    def unimplementedPluginBaseExtractorMethod(
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

        # TODO prepare your context here

        if len(input):
            # TODO your code for data coming in as arguments
            input = self.castOperand(input, SyncFHIRReference, "replace")
            result = self.getResources(input, resourceType="replace", raw=True)

        elif self.isFrame and not ignoreFrame:

            # TODO your code for data coming in as a frame
            if self.resourceTypeIs("Patient"):
                input = self.data

                result = input.apply(
                    lambda x: self.searchResources(
                        searchParams=dict(searchParams, **{"replace": x.id}),
                        resourceType="replace",
                        raw=True,
                    )
                )
                result = result.values

            elif self.resourceTypeIs("replace"):
                input = self.data.values
                result = self.getResources(input, resourceType="replace", raw=True)

            else:
                raise NotImplementedError

        elif searchActive:
            # TODO your code for searches
            result = self.searchResources(
                searchParams=searchParams, resourceType="replace", raw=True
            )

        else:
            raise NotImplementedError

        result = self.prepareOutput(result)

        return result
