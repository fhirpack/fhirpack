from cgitb import lookup
import json
import json
import importlib
from typing import Union

import pandas as pd

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference
import numpy as np
import fhirpack.utils as utils
import fhirpack.base

# LOGGER = CONFIG.getLogger(__name__)


class BaseTransformerMixin:
    def validate(
        self,
        references: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
    ):
        if references:
            references = self.prepareReferences(references)

        result = []
        if not references and self.isFrame:
            references = [e.to_reference() for e in self.data]
        elif references and not self.isFrame:
            pass
        elif references and self.isFrame:
            # TODO raise error references and isFrame not allowed
            # TODO raise in other similar methods
            pass

        references = self.referencesToResources(references)
        for ref in references:
            try:
                resourceType = ref["resourceType"]
                res = getattr(
                    importlib.import_module(f"fhir.resources.{resourceType.lower()}"),
                    resourceType,
                )

                obj = res.parse_obj(ref)
            except Exception as e:
                # TODO raise or log?
                return False
                pass

        # TODO what makes more sense, false or self?
        # TODO add guessResource type to prepareOutput when no resourceType given
        return self.prepareOutput(references)

    def gatherSimplePaths(
        self,
        paths: list[str],
        columns: list[str] = None,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        params: dict = {},
    ):
        """Extracts the elements from the given paths and returns them as a Frame.

        Args:
            paths (list[str]): Resource path to the desired elements.
            input (list[str], list[SyncFHIRReference], list[SyncFHIRResource], optional: Resources to operate on. If None, calling frame object will be used as input.
            params (dict): Additional parameters.

        Returns:
            Frame: FHIRPACK Frame object storing the resource elements in the respective rows.
        """
        if not params:
            params = {}
        if not columns:
            columns = paths

        if not input and self.isFrame:
            input = self.data.values
        elif input and not self.isFrame:
            input = self.prepareOperationInput(input, SyncFHIRResource)
        elif input and self.isFrame:
            # TODO your code for data coming in as arguments and frame
            raise NotImplementedError

        result = {k: [] for k in columns}

        for path, column in zip(paths, columns):
            # print(results)
            for element in input:
                if isinstance(element, SyncFHIRReference) or isinstance(
                    element, SyncFHIRResource
                ):
                    element = element.to_resource()
                elementResult = self.__gatherSimplePath(element, path)

                if elementResult.get(path, None):
                    result[column].append(elementResult[path])
                else:
                    result[column].append(None)
                # print(f"\n\n\n\n\n\n\n\n ..........result ...........")
                # print(json.dumps(results,indent=4,sort_keys=True))
        # return results
        # return pd.DataFrame(results)

        return self.prepareOutput(
            result, resourceType="Invalid", columns=columns, wrap=False
        )

    # TODO test path one level (no dot)
    # TODO test path two levels
    # TODO test path three levels

    # TODO test leaf is a list
    # pack.validate(
    # ['Patient/4137ebc9d2d745fbcf7ab6ea86d626a6d97096a3384dc53d666c3611c16b8136']
    # ).filterPaths(['name.given'])

    def __gatherSimplePath(self, data: dict, path: Union[str, list[str]]):
        if isinstance(path, str):
            frags = path.split(".")
        else:
            frags = path

        firstFrag = frags[0]
        # print(f"\n\n\n\n\n\n\n\n ..........entering {firstFrag}.....{len(frags)}")
        # print(json.dumps(data,indent=4,sort_keys=True))

        if isinstance(data, dict) and data.get(firstFrag):
            # print(f"dict........{frags}...{len(frags)}")
            if len(frags) == 1:
                # print(f"dict leaf ..... .....{frags}.....{len(frags)}")
                return {firstFrag: data[firstFrag]}
            else:
                # print(f"dict nonleaf ..... .....{frags}.....{len(frags)}")
                partialResults = self.__gatherSimplePath(data[firstFrag], frags[1:])
                # print(f"dict partial results ..........{frags}.....{len(frags)}")
                # print(json.dumps(partialResults,indent=4,sort_keys=True))
                results = {firstFrag + "." + k: v for k, v in partialResults.items()}
                # print(f"dict partial  ..........{frags}.....{len(frags)}")
                # print(json.dumps(results,indent=4,sort_keys=True))
                return results
        elif isinstance(data, list):
            results = {}
            for e in data:
                # print(f"list iter {e}........{frags}.......{len(frags)}")
                partialResults = self.__gatherSimplePath(e, frags)
                # print(f"list partial results ..........{frags}.....{len(frags)}")
                # print(json.dumps(partialResults,indent=4,sort_keys=True),'\n\n\n')
                # print(json.dumps(partialResults,indent=4,sort_keys=True),'\n\n\n')
                for k, v in partialResults.items():
                    # print('.............', k, v)
                    if results.get(k, None):
                        results[k].append(v)
                    else:
                        results[k] = [v]
                # print(f"list final results ..........{frags}.....{len(frags)}")
                # print(json.dumps(results,indent=4,sort_keys=True),'\n\n\n')
            return results
        # print(f"neither.........{frags}.......{len(frags)}")
        return {}

    # TODO test
    # pack.getPatients(
    # 	['Patient/4137ebc9d2d745fbcf7ab6ea86d626a6d97096a3384dc53d666c3611c16b8136'],
    #   includeLinkedPatients=True
    # ).gatherReferences(recursive=True)

    def gatherReferences(
        self,
        references: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        recursive: bool = False,
    ):
        """Extracts all the FHIR references as Resources from the input resources and returns them in a Frame.

        Args:
            references (Union[ list[str], list[SyncFHIRReference], list[SyncFHIRResource], ], optional): Input references. Defaults to None.
            recursive (bool, optional): If True, will recursively extract all the referenced Resources found in the given input. Defaults to False.

        Raises:
            NotImplementedError: If references and isFrame are both True.

        Returns:
            Frame: FHIRPACK Frame with the referencer and referencee of the references.
        """

        if references:
            references = self.prepareReferences(references)

        result = []
        if not references and self.isFrame:
            references = [e.to_reference() for e in self.data]
        elif references and not self.isFrame:
            pass
        elif references and self.isFrame:
            # TODO raise error references and isFrame not allowed
            # TODO raise in other similar methods
            raise NotImplementedError

        pending = references
        visited = []
        ret = []
        level = 0
        while len(pending) > 0:
            ref = pending.pop(0)
            if ref in visited:
                continue
            visited.append(ref)
            nrefs = []
            try:
                if not isinstance(ref, SyncFHIRReference):
                    ref = self.prepareReferences([ref])[0]
                nrefs = utils.valuesForKeys(ref.to_resource(), ["reference"])
            except Exception as e:
                print("Fatal error", e, "for ", ref, " referenced by ", visited[:-1])
            nrefs = list(nrefs)
            ret.append([ref, nrefs])
            level += 1
            if recursive:
                pending.extend(nrefs)
        return pd.DataFrame(ret, columns=["referencer", "referencee"])

    def gatherText(
        self,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        typeLookUps: list = None,
        lookUps: list = None,
        mapped: bool = False,
        includeMeta: bool = False,
        includeEmpty: bool = False,
        defaultLookUps: bool = True,
        includeDuplicates: bool = False,
    ):
        """Extracts text from resources by look-ups.

        Args:
            input: Data to extract text from.
            resourceType: The type is used the include type specific lookups.
            lookUps (list, optional): List of lookups to include in the text extraction.
            mapped (bool, optional): Store text labels as dictionary keys.
            includeMeta (bool, optional): Include the resource meta data.
            includeEmpty (bool, optional): Include empty Text for labels.
            defaultLookUps (bool, optional): Include the list of default Lookups.
            includeDuplicates (bool, optional): Include duplicated Test string.
        """

        input = [] if input is None else input
        lookUps = [] if lookUps is None else lookUps

        # default values that are optionally included in the text lookup
        if defaultLookUps:
            lookUps.extend(
                [
                    "display",
                    "summary",
                    "description",
                    "title",
                    "conclusion",
                    "note",
                    "text",
                    "answer",
                    "valueString",
                    "value",
                ]
            )

        if typeLookUps:
            # the file contains resource specific look ups
            with open(
                f"{utils.getInstallationPath()}/data/resourceTextElementMapping.json"
            ) as f:
                resourceLookUps = json.load(f)
                [lookUps.extend(resourceLookUps[t]) for t in typeLookUps]

        if input:
            input = self.castOperand(input, SyncFHIRResource)

        elif self.isFrame:
            input = self.data

        elif input and self.isFrame:
            # TODO raise error references and isFrame not allowed
            # TODO raise in other similar methods
            raise NotImplementedError

        result = []

        for resource in input:
            if not includeMeta:
                resource.pop("meta", None)

            if not mapped:
                text = []
                # TODO text representation is dependent of resource type, handle others and move to constants.py
                text.append(list(utils.valuesForKeys(resource, lookUps)))
                if not includeDuplicates:
                    text = list(set(utils.flattenList(text)))
                result.append(text)

            else:
                # text labels are stored as dictionary keys
                d = {}
                for k, v in resource.items():
                    d[k] = list(utils.valuesForKeys(v, lookUps))
                    if not includeDuplicates:
                        d[k] = list(set(d[k]))
                    if not includeEmpty and not d[k]:
                        d.pop(k)
                result.append([d])

        result = self.prepareOutput(result)

        return result

    def gatherKeys(
        self,
        params: dict = None,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
    ):
        """Extracts all keys(without values) found in the given input.

        Args:
            params (dict, optional): Parameters for the operation. Defaults to None.
            input (Union[list[str], list[SyncFHIRReference], list[SyncFHIRResource]], optional): Data to extract keys from. Defaults to None.

        Returns:
            DataFrame: DataFrame with the keys of the resources.
        """
        params = {} if params is None else params

        # TODO avoid converting provided resources into references and back
        # if references:
        # references = self.prepareReferences(references)

        if not input and self.isFrame:
            input = self.data
            pass
        elif input and not self.isFrame:
            input = self.prepareOperationInput(input, SyncFHIRResource)
            pass
        elif input and self.isFrame:
            # TODO raise error references and isFrame not allowed
            # TODO raise in other similar methods
            raise NotImplementedError

        result = []

        for i, e in input.items():
            e = e.serialize()
            result.append(list(utils.keys(e)))

        # return pd.DataFrame(pd.Series(result, dtype="object"), columns=["data"])
        return self.prepareOutput(result, resourceType="Invalid")

    def gatherValuesForKeys(
        self,
        keys: list[str],
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        params: dict = None,
    ):
        """Extracts the values(without keys) for the given keys from the input resources.

        Args:
            keys (list[str]): Keys to extract values for.
            input (Union[ list[str], list[SyncFHIRReference], list[SyncFHIRResource], ], optional): Data to extract values from. Defaults to None.
            params (dict, optional): Parameters for the operation. Defaults to None.

        Raises:
            NotImplementedError: If input and isFrame are provided.

        Returns:
            Union[list, pd.DataFrame]: List of values for keys.
        """
        params = {} if params is None else params

        # TODO avoid converting provided resources into references and back
        # if references:
        # references = self.prepareReferences(references)

        if not input and self.isFrame:
            input = self.data
            pass
        elif input and not self.isFrame:
            input = self.prepareOperationInput(input, SyncFHIRResource)
            pass
        elif input and self.isFrame:
            # TODO raise error references and isFrame not allowed
            # TODO raise in other similar methods
            raise NotImplementedError

        result = []

        for i, e in input.items():
            e = e.serialize()
            result.append(list(utils.valuesForKeys(e, keys)))

        # return pd.DataFrame(pd.Series(result, dtype="object"), columns=["values"])
        return self.prepareOutput(result, "Invalid")

    def gatherDates(
        self,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        recursive: bool = False,
        params: dict = None,
    ):
        """Extracts dates from resources.

        Args:
            input (Union[list[str], list[SyncFHIRReference], list[SyncFHIRResource]], optional): Data to extract dates from. Defaults to None.
            recursive (bool, optional): Whether to extract dates recursively. Defaults to False.
            params (dict, optional): Parameters for the operation. Defaults to None.

        Raises:
            NotImplementedError: If input and isFrame are provided.

        Returns:
            Union[list, pd.DataFrame]: List of dates.
        """
        params = {} if params is None else params

        # TODO avoid converting provided resources into references and back
        # if references:
        # references = self.prepareReferences(references)

        if not input and self.isFrame:
            input = self.data
            pass
        elif input and not self.isFrame:
            input = self.prepareOperationInput(input, SyncFHIRResource)
            pass
        elif input and self.isFrame:
            # TODO raise error references and isFrame not allowed
            # TODO raise in other similar methods
            raise NotImplementedError

        result = []

        for i, e in input.items():
            e = e.serialize()
            dates = list(
                # TODO move list of date-like elements to constants.py or infer them
                utils.valuesForKeys(
                    e,
                    [
                        "recordedDate",
                        "effectiveDate",
                        "issued",
                        "effectiveDateTime",
                    ],
                )
            )
            result.append(dates)
            # result.append([datetime.datetime.fromisoformat(d) for d in dates])

        result = pd.DataFrame(pd.Series(result), columns=["dates"])
        return result

        # TODO improve date parsing
        return pd.to_datetime(result.timestamp)
        (pd.Series(result, columns=["timestamp"]).to_datetime)
        # return pd.DataFrame(pd.Series(result,dtype="datetime64[ns]"),columns=["timestamp"])
