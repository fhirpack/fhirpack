from typing import Union
import numpy as np
from pandas import DataFrame
import json

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference

import fhirpack.extraction as extraction
import fhirpack.transformation as transformation
import fhirpack.load as load
import fhirpack.custom as custom

import fhirpack.utils as utils
from fhirpack.constants import CONFIG

LOGGER = CONFIG.getLogger(__name__)


class BaseMixin:

    # def __init__(self, client):
    # mixin methods should never have state of their own
    # otherwise the several levels of indirection make it
    # hard to understand the codebase
    # keep this class free of constructor, class variables
    # and similar

    def guessOutputResourceType(self, data):
        resourceType = None
        seenResourceTypes = None

        if data is not None:
            if isinstance(data[0], SyncFHIRReference) or isinstance(
                data[0], SyncFHIRResource
            ):
                seenResourceTypes = [e.resource_type for e in data]
                seenResourceTypes = set(seenResourceTypes)
            elif isinstance(data[0], dict):
                seenResourceTypes = [e["resourceType"] for e in data]
                seenResourceTypes = set(seenResourceTypes)

        if not seenResourceTypes:
            resourceType = "Uninitialized"
        elif len(seenResourceTypes) == 1:
            resourceType = seenResourceTypes.pop()
        else:
            resourceType = "Mixed"

        return resourceType

    def prepareCompositeOutput(self, data: dict):
        output = {}
        for resourceType, results in data.items():
            output[resourceType] = Frame(
                [[e] for e in results],
                # columns=['ref','raw'],
                # columns=["data"],
                resourceType=resourceType,
                client=self.client,
            )

        return output

    def prepareOutput(self, data, resourceType=None, columns=["data"], wrap=True):

        if len(data) and not resourceType:
            resourceType = self.guessOutputResourceType(data)

        if wrap:
            data = [[e] for e in data]
        output = Frame(
            data,
            columns=columns,
            resourceType=resourceType,
            client=self.client,
        )
        return output

    def parseReference(
        self, reference: Union[str, SyncFHIRReference], resourceType=None
    ):
        if isinstance(reference, str):
            if "/" in reference:
                res, resid = reference.split("/")
                if res and resid:
                    reference = self.client.reference(res, resid)
                else:
                    raise Exception(f"invalid reference format")
            else:
                if not resourceType:
                    resourceType = self.guessOutputResourceType(reference)
                reference = self.client.reference(resourceType, reference)
        elif isinstance(reference, SyncFHIRReference):
            reference.client = self.client
        return reference

    def prepareReferences(self, referenceList, resourceType=None):
        references = [self.parseReference(e, resourceType) for e in referenceList]
        return references

    def prepareOperationInput(self, input, target, resourceType=None):
        return self.castOperand(input, target, resourceType)

    def castOperand(self, input, target, resourceType=None):

        if isinstance(input, (list, np.ndarray, Frame)):
            pass
        else:
            input = [input]

        if isinstance(input, Frame):
            if target is Frame:
                return input
            elif target is SyncFHIRResource:
                result = [e.to_resource() for e in input.data.values]
                return result
            elif target is SyncFHIRReference:
                result = [e.to_reference() for e in input.data.values]
                return result

        elif isinstance(input[0], str):
            if target is str:
                return input
            elif target is SyncFHIRResource:
                input = self.prepareReferences(input, resourceType)
                result = self.castOperand(input, SyncFHIRResource)
                return result
            elif target is SyncFHIRReference:
                result = self.prepareReferences(input, resourceType)
                return result
            elif target is Frame:
                input = self.prepareOperationInput(
                    input, SyncFHIRReference, resourceType
                )
                result = self.prepareOOutput(input, resourceType)
                return result

        elif isinstance(input[0], SyncFHIRReference):

            if target is SyncFHIRReference:
                return input
            elif target is SyncFHIRResource:
                result = [e.to_resource() for e in input]
                return result
            elif target is Frame:
                result = self.prepareOutput(input, resourceType)
                return result

        elif isinstance(input[0], SyncFHIRResource):
            if target is SyncFHIRResource:
                return input
            elif target is Frame:
                result = self.prepareOutput(input, resourceType)
                return result
            elif target is SyncFHIRReference:
                result = [e.to_reference() for e in input]
                return result

    def referencesToIds(self, referenceList):
        return [e.id for e in referenceList]

    def referencesToResources(self, referenceList):
        return [e.to_resource() for e in referenceList]

    def prepareInput(self, data, resourceType):
        raise NotImplementedError

    # TODO: turn is frame into a property to avoid needing to call it everywhere ()
    @property
    def isFrame(self):
        return isinstance(self, Frame)


class Frame(
    DataFrame,
    BaseMixin,
    extraction.ExtractorMixin,
    transformation.TransformerMixin,
    load.LoaderMixin,
    custom.PluginMixin,
):

    _metadata = ["client", "resourceType"]

    def __init__(self, *args, **kwargs):
        # print(kwargs)
        self.client = kwargs.pop("client", None)
        self.resourceType = kwargs.pop("resourceType", None)

        super(Frame, self).__init__(*args, **kwargs)

    @property
    def _constructor(self):
        return Frame

    @property
    def _constructor_expanddim(self):
        return Frame

    # @property
    # def _constructor_sliced(self):
    #     return Frame

    @property
    def getResourceType(self):
        return self.resourceType

    def resourceTypeIs(self, resourceType):
        if self.resourceType:
            return resourceType.lower() == self.resourceType.lower()
        else:
            return False

    def setResourceType(self, resourceType):
        self.resourceType = resourceType
        return self

    # @property
    # def client(self):
    #     return self.CUSTOM_ARGS["client"]

    @property
    def pretty(self):
        for i, e in self.data.items():
            print(json.dumps(e, indent=4, sort_keys=True))

    @property
    def keys(self):
        for i, e in self.data.items():
            print(("\n").join(utils.keys(e)))

    # TODO report bug to pandas, explode doesn't preserve metadata
    def explode(self, *args, **kwargs):
        if not args:
            result = super().explode("data")
        else:
            result = super().explode(*args, **kwargs)
        result.client = self.client
        result.resourceType = self.resourceType
        return result

    def cast(self, format):
        if format == "frame":
            return self
        elif format == "list":
            return [list(t) for t in self.itertuples(index=False)]
        elif format == "dict":
            raise NotImplementedError
        elif format == "raw":
            return [list(t.data) for t in self.itertuples(index=False)]
