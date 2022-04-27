import json
from typing import Union

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference

import fhirdrill.custom.load.base as base

# TODO add your other load plugin classes here
import fhirdrill.custom.load.sample as sample


class PluginLoaderMixin(
    base.PluginBaseLoaderMixin,
    # TODO add your other load plugin classes here
    sample.PluginSampleLoaderMixin,
):

    # def __init__(self, client):
    # mixin methods should never have state of their own
    # otherwise the several levels of indirection make it
    # hard to understand the codebase
    # keep this class free of constructor, class variables
    # and similar
    pass
