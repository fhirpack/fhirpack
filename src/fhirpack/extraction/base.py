import json
from typing import Union
import time
import requests
from tqdm import tqdm
from dicomweb_client.api import DICOMwebClient

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference

import fhirpack
from fhirpack.constants import CONFIG


# TODO build dinamically from metadata/capability statement
SEARCH_PARAMS = {
    "Condition": [
        "_content",
        "_id",
        "_sort",
        "_include",
        "code",
        "identifier",
        "patient",
        "subject",
        "recordedDate__lt",
        "recordedDate__gt",
        "recordedDate__ge",
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
            result = self.prepareOutput(input)
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
        ignoreFrame: bool = False,
        raw: bool = False,
    ):

        searchActive = False if searchParams is None else True
        searchParams = {} if searchParams is None else searchParams

        params = {} if params is None else params
        input = [] if input is None else input

        result = []

        if len(input):
            pass

        elif self.isFrame and not ignoreFrame:
            input = self.data.values

        elif searchActive:
            raise NotImplementedError

        for element in tqdm(input, desc=f"GET[{resourceType}]> ", leave=False):
            element = self.castOperand(element, SyncFHIRResource, resourceType)
            result.extend(element)

        if not raw:
            result = self.prepareOutput(result)

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
        ignoreFrame: bool = True,
        raw: bool = False,
    ):

        searchActive = False if searchParams is None else True
        searchParams = {} if searchParams is None else searchParams

        params = {} if params is None else params
        input = [] if input is None else input

        if searchParams:

            invalidsearchParams = set(searchParams.keys()) - set(
                SEARCH_PARAMS[resourceType]
            )
            if invalidsearchParams:
                raise Exception(f"non allowed search parameters {invalidsearchParams}")

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
                if not resourceCount:
                    resourceCount = search.count()

                for element in tqdm(
                    search,
                    desc=f"SEARCH[{resourceType}]> ",
                    total=resourceCount,
                    leave=False,
                ):
                    result.append(element)
            except:
                # server doesn't support _total parameter nor returns total
                # element in each request https://build.fhir.org/bundle.html#searchset
                pass

        if not raw:
            result = self.prepareOutput(result, resourceType)

        return result

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

            result = fhirpack.PACK().searchResources(
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
                # TODO log to execution.log
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
