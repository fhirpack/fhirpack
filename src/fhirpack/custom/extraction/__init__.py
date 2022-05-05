import json
from typing import Union

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference

import fhirpack.custom.extraction.base as base

# TODO add your other extraction plugin classes here
import fhirpack.custom.extraction.sample as sample
import fhirpack.custom.extraction.ship as ship


class PluginExtractorMixin(
    # TODO add your other extraction plugin classes here
    sample.PluginSampleExtractorMixin,
    ship.PluginSHIPExtractorMixin,
):

    # def __init__(self, client):
    # mixin methods should never have state of their own
    # otherwise the several levels of indirection make it
    # hard to understand the codebase
    # keep this class free of constructor, class variables
    # and similar
    pass
