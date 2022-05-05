import json
from typing import Union

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference

import fhirpack.custom.transformation.base as base

# TODO add your other transformation plugin classes here
import fhirpack.custom.transformation.sample as sample


class PluginTransformerMixin(
    base.PluginBaseTransformerMixin,
    # TODO add your other transformation plugin classes here
    sample.PluginSampleTransformerMixin,
):

    # def __init__(self, client):
    # mixin methods should never have state of their own
    # otherwise the several levels of indirection make it
    # hard to understand the codebase
    # keep this class free of constructor, class variables
    # and similar
    pass
