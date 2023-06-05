from typing import Union
import numpy as np
from pandas import DataFrame
import pandas as pd
import json

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference

import fhirpack.pack as pack
import fhirpack.extraction as extraction
import fhirpack.transformation as transformation
import fhirpack.load as load
import fhirpack.custom as custom
import fhirpack.utils as utils
from fhirpack.constants import CONFIG

LOGGER = CONFIG.getLogger(__name__)

SIMPLE_PATHS = {
    "default": ["id"],
    "Reference": ["resourceType"],
    "Patient": [
        "name.given",
        "name.family",
        "birthDate",
        "city",
        "state",
        "country",
    ],
    "DiagnosticReport": [
        "subject",
        "presentedForm.contentType",
        "presentedForm.data",
        "presentedForm.url",
        "presentedForm.title",
        "presentedForm.creation",
    ],
    "Observation": [
        "subject",
        "category.coding.code",
        "code.coding.display",
        "code.coding.code",
        "valueQuantity.value",
    ],
}


class BaseMixin:
    """Base class with methods that are avaialable to all Frame
    objects and operations according to the mixin pattern.
    The methods are not directly associated with the Extractor, Transformer
    or Loader.
    """

    # def __init__(self, client):
    # mixin methods should never have state of their own
    # otherwise the several levels of indirection make it
    # hard to understand the codebase
    # keep this class free of constructor, class variables
    # and similar

    resourceType = "Invalid"

    def guessOutputResourceType(self, data):
        """Guess the resource type of the data received.

        Args:
            data: Data to be processed.

        Returns:
            str: Resource type of the output data.
        """
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
        """Constructs a composite Frame, that is a frame containing
        multiple resource types, from the provided data.

        Args:
            data (dict): Data stored in the Frame object.

        Returns:
            Frame: Frame object storing the provided data.
        """
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
        """Constructs a Frame object from the provided data.

        Args:
            data: Data stored in the Frame object.
            resourceType: FHIR resource type of the provided data.
            columns: Colunn names. Defaults to ["data"].
            wrap: Defaults to True.

        Returns:
            Frame: Frame object storing the provided data.
        """

        if len(data) and not resourceType:
            resourceType = self.guessOutputResourceType(data)

        if wrap:
            data = [[e] for e in data]

        output = Frame(
            data,
            columns=columns,
            resourceType=resourceType,
            client=self.client,
            # **frameParams
        )

        return output

    def attachOperandIds(self, input, result, metaResourceType):
        """Attaches the ids of the input data to the result data.

        Args:
            input (_type_): _description_
            result (_type_): _description_
            metaResourceType (_type_): _description_

        Returns:
            _type_: _description_
        """
        sourceType = input.resourceType

        # the target type is the desired resource type
        # getPatients().getConditions() -> "Patient" source, "Condition" target
        targetType = result.resourceType
        targetType = metaResourceType

        # TODO: improve empty result handling
        result[result.resourceType] = result.gatherSimplePaths(["id"])
        result = result.drop_duplicates(subset=[result.resourceType])

        if sourceType in ["Invalid", "Reference"] or sourceType == targetType:
            return input, result

        field, basePath = input.getConversionPath(
            sourceType=sourceType, targetType=targetType
        )

        path = "id" if basePath is None else f"{basePath}.id"

        searchValues = input.gatherSimplePaths([path], columns=["searchValue"]).dropna()

        if not searchValues.size:
            path = f"{basePath}.reference"

        if input.isFrame and input.resourceType != "Invalid":
            baseReversePath = None
            try:
                reverseField, baseReversePath = self.getConversionPath(
                    sourceType=targetType, targetType=sourceType
                )
                reversePath = (
                    "id" if baseReversePath is None else f"{baseReversePath}.id"
                )

                searchValues = result.gatherSimplePaths(
                    [reversePath], columns=["searchValue"]
                ).dropna()

                if not searchValues.size:
                    reversePath = f"{baseReversePath}.reference"
            except:
                pass

            # contained=True means it's possible to access the resources
            # which form the basis for the search from the result resources
            containedReverse = True

            # if this is not possible, a join is necessary based on the
            # resources which form the basis of the search
            if baseReversePath is None:
                containedReverse = False

            if containedReverse:
                result[input.resourceType] = result.gatherSimplePaths([reversePath])[
                    reversePath
                ].values

                # if the reverse-matching path contains lists as in link.other
                # we use .any() because not each of the root patients has linked patients
                if (
                    result[input.resourceType].apply(type).astype(str)
                    == "<class 'list'>"
                ).any():
                    result = result.explode(input.resourceType)
                    # result[input.resourceType] = result[input.resourceType].apply(lambda x: x.id)

                if "reference" in reversePath:
                    result[input.resourceType] = result[input.resourceType].apply(
                        lambda x: None if x is None else x.split("/")[-1]
                    )

            else:
                # print(f"calculating {result.resourceType} using {path}")
                input[result.resourceType] = input.gatherSimplePaths([path])[
                    path
                ].values

                # if the reverse-matching path contains lists as in link.other
                # we use .any() because not each of the root patients has linked patients
                if (
                    input[result.resourceType].apply(type).astype(str)
                    == "<class 'list'>"
                ).any():
                    input = input.explode(result.resourceType)
                    # input[result.resourceType] =input[result.resourceType].apply(lambda x:x.id)

                if "reference" in path:
                    input[result.resourceType] = input[result.resourceType].apply(
                        lambda x: None if x is None else x.split("/")[-1]
                    )

                # print(f"joining frame with {result.columns}({result.index}) and frame with {input.columns} on {result.resourceType}","\n")
                # print(input.to_dict(),"\n")
                # print(result.to_dict(),"\n")
                # result = input.join(result,on=result.resourceType,how='inner', rsuffix='_self')
                result = pd.merge(
                    result, input, on=result.resourceType, suffixes=["", "_input"]
                )
                # result=result.combine_first(input)
                # result[input.resourceType]=input.gatherSimplePaths([path])[path].values

                result.drop(columns=["data_input"], inplace=True)

        return input, result

    def parseReference(
        self, reference: Union[str, SyncFHIRReference], resourceType: str = None
    ):
        """Parses a reference string into a SyncFHIRReference object.

        Args:
            reference (Union[str, SyncFHIRReference]): Input reference string or SyncFHIRReference object.
            resourceType (str, optional): Resource type of the reference. Defaults to None.

        Raises:
            Exception: If the reference string is not in the correct format.

        Returns:
            _type_: _description_
        """
        if isinstance(reference, str):
            if "/" in reference:
                res, resid = reference.split("/")
                if (
                    res and resid
                ):  # this assumes that format ist always resourceType/id which is not always the case
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

    def prepareReferences(self, referenceList, resourceType: str = None):
        """Parses a list of references into a list of SyncFHIRReference objects.

        Args:
            referenceList (list): List of reference strings or SyncFHIRReference objects.
            resourceType (_type_, optional): Resource type of the references. Defaults to None.

        Returns:
            list[SyncFHIRReference]: List of SyncFHIRReference objects.
        """
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

    def referencesToIds(self, referenceList: list[SyncFHIRReference]) -> list[str]:
        """Converts a list of SyncFHIRReference objects into a list of ids.

        Args:
            referenceList (list[SyncFHIRReference]): List of SyncFHIRReference objects.

        Returns:
            list[str]: List of ids.
        """
        return [e.id for e in referenceList]

    def referencesToResources(self, referenceList):
        return [e.to_resource() for e in referenceList]

    def prepareInput(self, data, resourceType):
        raise NotImplementedError

    @property
    def isFrame(self):
        return isinstance(self, Frame)

    @property
    def connected(self):
        try:
            self.client._do_request("get", f"{self.client.url}/metadata")
            return True
        except:
            return False

    def authenticate(self, force: bool = False):
        if not self.connected or force:
            self.client = pack._getConnectedClient()


class Frame(
    DataFrame,
    BaseMixin,
    extraction.ExtractorMixin,
    transformation.TransformerMixin,
    load.LoaderMixin,
    custom.PluginMixin,
):
    """This is the main datatstructure of the FHIRPACK package. It inherits from pandas.DataFrame
    and adds the functionality to work with FHIR resources.
    """

    _metadata = [
        "client",
        "resourceType",
        "apibase",
    ]

    def __init__(self, *args, **kwargs):
        """Initializes a Frame object."""
        # print(kwargs)
        self.client = kwargs.pop("client", None)
        self.resourceType = kwargs.pop("resourceType", None)

        super(Frame, self).__init__(*args, **kwargs)

    @property
    def _constructor(self):
        def _c(*args, **kwargs):
            return Frame(*args, **kwargs).__finalize__(self)

        return _c

        # return Frame

    @property
    def _constructor_expanddim(self):
        return Frame

    # @property
    # def _constructor_sliced(self):
    #     return Frame

    @property
    def getResourceType(self):
        return self.resourceType

    def resourceTypeIs(self, resourceType: str) -> bool:
        """Returns True if the resourceType of the Frame object matches the given resourceType.

        Args:
            resourceType (str): Resource type to compare.

        Returns:
            bool: True if the resourceType of the Frame object matches the given resourceType.
        """
        if self.resourceType:
            return resourceType.lower() == self.resourceType.lower()
        else:
            return False

    def setResourceType(self, resourceType: str):
        """Sets the resourceType of the Frame object.

        Args:
            resourceType (str): Resource type to set.
        """
        self.resourceType = resourceType
        return self

    # @property
    # def client(self):
    #     return self.CUSTOM_ARGS["client"]

    @property
    def pretty(self):
        """Prints the Frame object in a pretty json format."""
        print(json.dumps(self.data.values.tolist(), indent=4, sort_keys=True))

    @property
    def summary(self):
        """Prints a summary of the Frame object.

        Returns:
            Frame: Summary of the Frame object.
        """
        return self.gatherSimplePaths(
            SIMPLE_PATHS["default"] + SIMPLE_PATHS.get(self.resourceType, [])
        )

    @property
    def keys(self):
        for i, e in self.data.items():
            print(("\n").join(utils.keys(e)))

    # TODO report bug to pandas, explode doesn't preserve metadata
    def explode(self, *args, **kwargs):
        """Explodes all lists in the Frame object.

        Returns:
            Frame: Exploded Frame object.
        """
        if not args:
            result = super().explode("data")
        else:
            result = super().explode(*args, **kwargs)
        result.client = self.client
        result.resourceType = self.resourceType
        return result

    def cast(self, format):
        """Casts the Frame object to a different format.

        Args:
            format (str): Format to cast to.

        Raises:
            NotImplementedError: If the format is not implemented.
        """
        if format == "frame":
            return self
        elif format == "list":
            return [list(t) for t in self.itertuples(index=False)]
        elif format == "dict":
            raise NotImplementedError
        elif format == "raw":
            return [list(t.data) for t in self.itertuples(index=False)]
