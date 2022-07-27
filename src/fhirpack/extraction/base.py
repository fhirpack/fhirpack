import chunk
import math
import json
from typing import Union
import time
import requests
from tqdm import tqdm
from dicomweb_client.api import DICOMwebClient
import pandas as pd

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference

import fhirpack
from fhirpack.constants import CONFIG


# TODO build dinamically from metadata/capability statement
SEARCH_PARAMS = {
    "Condition": [  # https://www.hl7.org/fhir/condition.html
        "_content",
        "_id",
        "_sort",
        "_include",
        "code",
        "identifier",
        "patient",
        "subject",
        "recorded-date__eq",
        "recorded-date__lt",
        "recorded-date__gt",
        "recorded-date__ge",
    ],
    "EpisodeOfCare": [
        "_id",
        "_content",
        "_sort",
        "_include",
        "code",
        "identifier",
        "patient",
    ],
    "Encounter": [
        "_id",
        "_content",
        "_sort",
        "_include",
        "code",
        "identifier",
        "subject",
    ],
    "DiagnosticReport": [
        "_id",
        "_content",
        "_sort",
        "_include",
        "code",
        "identifier",
        "subject",
        "issued",
        "category",
        "encounter",
        "issued__lt",
        "issued__gt",
        "issued__ge",
        "date__lt",
        "date__gt",
        "date__ge",
    ],
    "DocumentReference": [
        "_id",
        "_content",
        "_sort",
        "_include",
        "code",
        "identifier",
        "subject",
        "category",
        "date",
        "contenttype",
        "description",
        "location",
        "patient",
        "related",
        "relatesto",
        "status",
        "type",
    ],
    "FamilyMemberHistory": [
        "_content",
        "_id",
        "_sort",
        "_include",
        "code",
        "identifier",
        "patient",
        "_content",
    ],
    "MedicationAdministration": [
        "_content",
        "_id",
        "_sort",
        "_include",
        "code",
        "identifier",
        "subject",
    ],
    "MedicationRequest": [
        "_id",
        "_content",
        "_sort",
        "_include",
        "code",
        "identifier",
        "subject",
    ],
    "Observation": [
        "_content",
        "_id",
        "_sort",
        "_include",
        "code",
        "_count",
        "__count",
        "count",
        "identifier",
        "patient",
    ],
    "Patient": [
        "_content",
        "_id",
        "_sort",
        "_include",
        "code",
        "identifier",
        "given",
        "family",
        "name",
        "link",
        "link:missing",
    ],
    "ImagingStudy": [
        "_content",
        "_id",
        "_sort",
        "_include",
        "code",
        "identifier",
        "subject",
        "endpoint:missing",
        "shipProcedureCode",
    ],
    "Procedure": [
        "_id",
        "_content",
        "_sort",
        "_include",
        "code",
        "identifier",
        "subject",
    ],
    "List": ["_id", "_content", "_sort", "_include", "code", "identifier"],
}

META_RESOURCE_TYPES = {"RootPatient": "Patient", "LinkedPatient": "Patient"}

# first key is source resourcetype
# second key is destination resourcetype
# field is by what to search in destination resourcetype
# path is where to find the values to search in field
# path: None means id

SEARCH_ATTRIBUTES = {
    "Patient": {
        "Condition": {"field": "subject", "path": None},
        "DiagnosticReport": {"field": "subject", "path": None},
        "EpisodeOfCare": {"field": "patient", "path": None},
        "Encounter": {"field": "patient", "path": None},
        "FamilyMemberHistory": {"field": "_content", "path": None},
        "ImagingStudy": {"field": "subject", "path": None},
        "List": {"field": "", "path": None},
        "MedicationAdministration": {"field": "subject", "path": None},
        "MedicationRequest": {"field": "subject", "path": None},
        "Observation": {"field": "patient", "path": None},
        "Procedure": {"field": "patient", "path": None},
        "RootPatient": {"field": "link", "path": None},
        "LinkedPatient": {"field": "_id", "path": None},
    },
    "RootPatient": {
        "Patient": {"field": "_id", "path": "link.other"},
        "LinkedPatient": {"field": "_id", "path": "link.other"},
        # "LinkedPatient": {"field": "_id", "path": None}
    },
    "LinkedPatient": {
        # "Patient": {"field": "_id", "path": "link.other"}
        # "RootPatient": {"field": "_id", "path": None},
        "Patient": {"field": "_id", "path": "id"}
    },
    "ImagingStudy": {"Patient": {"field": "_id", "path": "subject"}},
    "Condition": {
        "Patient": {"field": "_id", "path": "subject"},
        "LinkedPatient": {"field": "_id", "path": "subject"},
        "RootPatient": {"field": "_id", "path": "subject"},
        "Encounter": {"field": "_id", "path": "encounter"},
    },
    "Observation": {
        "Patient": {"field": "_id", "path": "subject"},
        "RootPatient": {"field": "_id", "path": "subject"},
        "LinkedPatient": {"field": "_id", "path": "subject"},
        "Encounter": {"field": "_id", "path": "encounter"},
    },
    "MedicationAdministration": {
        "Patient": {"field": "_id", "path": "subject"},
        "RootPatient": {"field": "_id", "path": "subject"},
        "LinkedPatient": {"field": "_id", "path": "subject"},
    },
    "DiagnosticReport": {
        "Patient": {"field": "_id", "path": "subject"},
        "RootPatient": {"field": "_id", "path": "subject"},
        "LinkedPatient": {"field": "_id", "path": "subject"},
    },
    "AllergyIntolerance": {"Patient": {"field": "_id", "path": "patient"}},
    "CarePlan": {
        "Patient": {"field": "_id", "path": "subject"},
        "RootPatient": {"field": "_id", "path": "subject"},
        "LinkedPatient": {"field": "_id", "path": "subject"},
    },
    "CarePlan": {
        "Patient": {"field": "_id", "path": "subject"},
        "RootPatient": {"field": "_id", "path": "subject"},
        "LinkedPatient": {"field": "_id", "path": "subject"},
    },
    "Claim": {
        "Patient": {"field": "_id", "path": "subject"},
        "RootPatient": {"field": "_id", "path": "subject"},
        "LinkedPatient": {"field": "_id", "path": "subject"},
    },
    "Encounter": {
        "Patient": {"field": "_id", "path": "subject"},
        "RootPatient": {"field": "_id", "path": "subject"},
        "LinkedPatient": {"field": "_id", "path": "subject"},
    },
    "EpisodeOfCare": {
        "Patient": {"field": "_id", "path": "subject"},
        "RootPatient": {"field": "_id", "path": "subject"},
        "LinkedPatient": {"field": "_id", "path": "subject"},
    },
    "Goal": {
        "Patient": {"field": "_id", "path": "subject"},
        "RootPatient": {"field": "_id", "path": "subject"},
        "LinkedPatient": {"field": "_id", "path": "subject"},
    },
    "Immunization": {
        "Patient": {"field": "_id", "path": "patient"},
        "RootPatient": {"field": "_id", "path": "subject"},
        "LinkedPatient": {"field": "_id", "path": "subject"},
    },
    "Procedure": {
        "Patient": {"field": "_id", "path": "subject"},
        "RootPatient": {"field": "_id", "path": "subject"},
        "LinkedPatient": {"field": "_id", "path": "subject"},
    },
}


class BaseExtractorMixin:
    def getReferences(
        self,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        params: dict = None,
        ignoreFrame: bool = False,
        raw: bool = False,
    ):

        params = {} if params is None else params

        if not input and self.isFrame:
            input = self.data
            pass
        elif input and not self.isFrame:
            input = self.prepareOperationInput(input, SyncFHIRReference)
            pass
        elif input and self.isFrame:
            # TODO raise error references and isFrame not allowed
            # TODO raise in other similar methods
            raise NotImplementedError

        if not raw:
            result = self.prepareOutput(input, resourceType="Reference")
        return result

    def getResources(
        self,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        searchParams: dict = None,
        params: dict = None,
        resourceType: str = None,
        metaResourceType: str = None,
        ignoreFrame: bool = False,
        raw: bool = False,
        progressSuffix: str = "",
    ):

        if metaResourceType is None:
            metaResourceType = resourceType

        searchActive = False if searchParams is None else True
        searchParams = {} if searchParams is None else searchParams

        params = {} if params is None else params
        input = [] if input is None else input

        searchValues = []
        result = []

        if len(input):
            inputReprs = set()
            uniqueInput = []
            for i in input:
                r = repr(i)
                if r not in inputReprs:
                    uniqueInput.append(i)
                    inputReprs.update([r])
            input = uniqueInput

            for element in tqdm(
                input, desc=f"GET[{metaResourceType}]{progressSuffix}> ", leave=False
            ):
                element = self.castOperand(element, SyncFHIRResource, resourceType)
                result.extend(element)

        elif self.isFrame and not ignoreFrame:
            # utils.validateFrame(self)
            input = self.data

            # source Type is the type of resources contained in a frame
            sourceType = self.resourceType

            # the target type is the desired resource type
            # getPatients().getConditions() -> "Patient" source, "Condition" target
            targetType = resourceType

            # handles
            # pack.getReferences().getResources
            # pack.getReferences().getResources
            if targetType is None:
                return self.getResources(self.data.values)

            field, basePath = self.getConversionPath(
                sourceType=sourceType, targetType=metaResourceType
            )

            path = "id" if basePath is None else f"{basePath}.id"

            searchValues = self.gatherSimplePaths(
                [path], columns=["searchValue"]
            ).dropna()

            if not searchValues.size:
                path = f"{basePath}.reference"
                searchValues = self.gatherSimplePaths([path], columns=["searchValue"])

            if (
                searchValues["searchValue"].apply(type).astype(str) == "<class 'list'>"
            ).any(0):
                searchValues = searchValues.explode("searchValue")

            searchValues = searchValues.dropna()

            if "reference" in path:
                searchValues = searchValues["searchValue"].str.split("/").str[-1]
            else:
                searchValues = searchValues["searchValue"].values

        elif searchActive:
            # getResources is for getting/searching known resources
            # delegate to search for special handling

            return self.searchResources(
                input=input,
                searchParams=searchParams,
                params=params,
                ignoreFrame=ignoreFrame,
                resourceType=resourceType,
            )

        n = len(searchValues)
        chunkSize = 100
        nChunks = math.ceil(n / chunkSize)
        i, j = 0, 0

        total = []

        while j < n:

            j = j + chunkSize if j + chunkSize < n else n

            searchValuesChunk = searchValues[i:j]
            searchValuesChunk = ",".join(searchValuesChunk)
            searchParams.update({field: searchValuesChunk})

            result += self.searchResources(
                searchParams=searchParams,
                resourceType=resourceType,
                raw=True,
                progressSuffix=f"({math.ceil(j/chunkSize)}/{nChunks})",
            )
            i = i + chunkSize

        if not raw:
            indexList = []
            result = self.prepareOutput(result, resourceType=resourceType)
            input, result = self.attachOperandIds(self, result, metaResourceType)

        return result

    def searchResources(
        self,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        searchParams: dict = None,
        params: dict = None,
        resourceType: str = None,
        metaResourceType: str = None,
        ignoreFrame: bool = True,
        raw: bool = False,
        progressSuffix: str = "",
    ):

        if metaResourceType is None:
            metaResourceType = resourceType

        searchActive = False if searchParams is None else True
        searchParams = {} if searchParams is None else searchParams

        params = {} if params is None else params
        input = [] if input is None else input

        # if searchParams:

        #     invalidsearchParams = set(searchParams.keys()) - set(
        #         SEARCH_PARAMS[resourceType]
        #     )
        #     if invalidsearchParams:
        #         raise Exception(f"non allowed search parameters {invalidsearchParams}")

        if len(input):
            raise NotImplementedError

        elif self.isFrame and not ignoreFrame:
            raise NotImplementedError

        elif searchActive:
            pass

        resourcePageSize = 100

        search = (
            self.client.resources(resourceType)
            .search(**searchParams)
            .limit(resourcePageSize)
        )
        result = []
        resourceCount = 0
        nonEmptyBundle = bool(len(search.limit(1).fetch()))

        if nonEmptyBundle:
            try:
                resourceCount = search.limit(1).fetch_raw().get("total", None)
            except:
                # server doesn't support _total parameter nor returns total
                # element in each request https://build.fhir.org/bundle.html#searchset
                pass
            if not resourceCount:
                resourceCount = search.count()
            for element in tqdm(
                search,
                desc=f"SEARCH[{metaResourceType}]{progressSuffix}> ",
                total=resourceCount,
                leave=False,
            ):
                result.append(element)

        if not raw:
            result = self.prepareOutput(result, resourceType)
            input, result = self.attachOperandIds(self, result, metaResourceType)

        return result

    def getConversionPath(self, sourceType: str, targetType: str):
        """This method retrieves the needed fhir serach param (field) and the
        respective path for a source-target pair from the handler ditcionary"""

        sourceDict = SEARCH_ATTRIBUTES.get(sourceType, {})
        targetDict = sourceDict.get(targetType, {})
        field, path = targetDict.get("field"), targetDict.get("path")

        if field:  # and path:
            return field, path
        else:
            aliasSourceDict = SEARCH_ATTRIBUTES.get(META_RESOURCE_TYPES[sourceType], {})
            aliasTargetDict = aliasSourceDict.get(targetType, {})
            aliasField, aliasPath = aliasTargetDict.get("field"), targetDict.get("path")
            if aliasField:
                return aliasField, aliasPath

            raise RuntimeError(
                f"No handler for source {sourceType} and target {targetType}"
            )

    def getAbsolutePaths(
        self,
        paths: list[str],
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        searchParams: dict = None,
        params: dict = None,
    ):

        searchActive = False if searchParams is None else True
        searchParams = {} if searchParams is None else searchParams

        params = {} if params is None else params
        input = [] if input is None else input

        # invalidsearchParams = None
        # if searchParams:
        #     invalidsearchParams = set(searchParams.keys()) - set(
        #         base.SEARCH_PARAMS["MedicationAdministration"]
        #     )

        # if invalidsearchParams:
        #     raise Exception(f"non allowed search parameters {invalidsearchParams}")

        if not input and self.isFrame:
            input = self.data
        elif input and not self.isFrame:
            raise NotImplementedError
        elif input and self.isFrame:
            raise NotImplementedError

        if self.resourceTypeIs("patient"):
            searchParams["subject"] = ",".join([e.id for e in self.data])
        else:
            raise NotImplementedError

        finalResults = {}

        # TODO move allowed absolute paths allowed for patients somewhere else
        # these relative paths are allowed because they reference a subject or patient
        relativePaths = {
            "Appointment": [],
            "CarePlan": [],
            "ClinicalImpression": [],
            "Condition": [],
            "DiagnosticReport": [],
            "DocumentReference": [],
            "Encounter": [],
            "EpisodeOfCare": [],
            "ImagingStudy": [],
            "Immunization": [],
            "List": [],
            "MedicationRequest": [],
            "MedicationStatement": [],
            "Observation": [],
            "Procedure": [],
            "QuestionnaireResponse": [],
            "ServiceRequest": [],
            # 'BiologicallyDerivedProduct':[],
            # 'DocumentReference':[],
            # 'FamilyMemberHistory':[],
            # 'Media':[],
            # 'Medication':[],
            # 'MedicationAdministration':[],
            # 'Organization':[],
            # 'Patient':[],
            # 'Practitioner':[],
            # 'Specimen':[],
            # 'Substance':[]
        }

        paths = [e.split(".") for e in sorted(paths)]
        for absp in paths:
            relativePaths[absp[0]].append(absp[1:])

        resourceType = self.resourceType

        for resourceType, relpaths in relativePaths.items():
            if not relpaths:
                continue

            result = self.searchResources(
                resourceType=resourceType, searchParams=searchParams
            )
            n = len(result)
            filteredResults = []

            # TODO handle multiple filters
            # filter = filter.popitem()

            filteredResults = result.gatherSimplePaths([".".join(e) for e in relpaths])
            filteredResults.columns = [
                resourceType + "." + key for key in filteredResults.columns
            ]

            # filteredRecord.update({f"{resourceType}.{filter[0]}": filter[1]})
            # filteredResults.append(filteredRecord)

            finalResults[resourceType] = filteredResults

        return finalResults

    def getURLBytes(
        self,
        input: list[str] = None,
        operateOnCol: str = "data",
        resultInCol: str = None,
        params: dict = {},
    ):

        params = {} if params is None else params
        input = [] if input is None else input

        if not input and self.isFrame:
            if operateOnCol:
                input = self[operateOnCol].values
            elif self.resourceTypeIs("DiagnosticReport"):
                input = self.gatherSimplePaths(["presentedForm.url"])
            else:
                raise NotImplementedError
        elif input and not self.isFrame:
            raise NotImplementedError
        elif input and self.isFrame:
            raise NotImplementedError

        results = []
        for i, url in zip(range(len(input)), input):
            response = requests.get(
                url,
                headers=self.client._build_request_headers(),
                stream=True,
            )

            data = bytearray()

            if not response.ok:
                # TODO log to fhirpack.log
                data = None
                # raise Exception(f"{response}")
            else:
                for block in response.iter_content(1024):
                    data.extend(block)
                    if not block:
                        break

            time.sleep(0.5)
            results.append(data)
        if resultInCol:
            result = self.assign(**{resultInCol: results})
        else:
            result = self.prepareOutput(results, "Binary")
        return result

    def getFromFiles(self, input: list[str]):
        """Creates a Frame object from json files containing fhir resources"""

        pathsData = []
        for iPath in input:
            with open(iPath, "r") as f:
                rawJson = json.load(f)
                fileData = []
                if isinstance(rawJson, list):
                    fileData.extend(rawJson)
                elif rawJson["resourceType"] == "Bundle":
                    for r in rawJson["entry"]:
                        fileData.append(r["resource"])
                else:
                    fileData.append(rawJson)
            pathsData.extend(fileData)

        for element in pathsData:
            if element["resourceType"] != pathsData[0]["resourceType"]:
                raise TypeError("All resources have to be of the same type.")

        result = [
            SyncFHIRResource(self.client, e["resourceType"], **e) for e in pathsData
        ]
        result = self.prepareOutput(result)
        return result

    def getDICOMInstances(
        self,
        input: list[str] = None,
        operateOnCol: str = "data",
        resultInCol: str = None,
        params: dict = None,
        inPlace: dict = False,
    ):

        params = {} if params is None else params
        input = [] if input is None else input

        if not input and self.isFrame:
            if self.resourceTypeIs("ImagingStudy"):
                input = self
            else:
                raise NotImplementedError
        elif input and not self.isFrame:
            raise NotImplementedError
        elif input and self.isFrame:
            raise NotImplementedError

        result = []

        for i, series, study, endpoint in input[
            ["series", "study", "endpoint"]
        ].itertuples():
            client = DICOMwebClient(
                endpoint,
                headers={
                    "Authorization": f"Bearer {CONFIG.get('EXTRACTION_BASE_TOKEN_DICOM')}"
                },
            )
            instances = list(client.iter_series(study, series))
            result.append(instances)

        if inPlace:
            self.data = result
            result = self
        else:
            result = self.prepareOutput(result)

        return result
