import fhirpack.custom.extraction as extraction
import fhirpack.custom.transformation as transformation
import fhirpack.custom.load as load


class PluginMixin(
    extraction.PluginExtractorMixin,
    transformation.PluginTransformerMixin,
    load.PluginLoaderMixin,
):

    # def __init__(self, client):
    # mixin methods should never have state of their own
    # otherwise the several levels of indirection make it
    # hard to understand the codebase
    # keep this class free of constructor, class variables
    # and similar
    pass
