import json
import importlib
from typing import Union

import pandas as pd

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference

import fhirpack.utils as utils


class PluginBaseMixin:
    def unimplementedPluginBaseMethod(
        self,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        params: dict = None,
        ignoreFrame: bool = False,
    ):

        params = {} if params is None else params
        input = [] if input is None else input
        result = []

        # TODO prepare your context here

        if len(input):
            # TODO your code for data coming in as arguments
            pass

        elif self.isFrame and not ignoreFrame:

            # TODO your code for data coming in as a frame
            if self.resourceTypeIs("Patient"):
                input = self.data
                result = input.values

            elif self.resourceTypeIs("replace"):
                input = self.data
                result = input.values

            else:
                raise NotImplementedError

        else:
            raise NotImplementedError

        result = self.prepareOutput(result)

        return result
