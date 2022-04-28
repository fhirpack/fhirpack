from abc import abstractmethod
import json
import resource
from typing import Union
import time
import requests
import magic
import numpy as np
import math
from tqdm import tqdm

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference

import fhirdrill
from fhirdrill.constants import CONFIG


from dicomweb_client.api import DICOMwebClient
import os
from pathlib import Path

client = DICOMwebClient(
    "https://shipdev.uk-essen.de/app/DicomWeb/view/deidentified/GEPACS",
    headers={"Authorization": "Bearer {}".format(CONFIG.get("OAUTH_TOKEN"))},
)


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
        "date" ,
        "date__lt",
        "date__gt"
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
    ],
    "ImagingStudy": [
        "_content",
        "_id",
        "_sort",
        "_include",
        "code",
        "identifier",
        "subject",
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

        if input:
            pass

        elif self.isFrame and not ignoreFrame:
            input = self.data.values

        elif searchActive:
            raise NotImplementedError

        for element in tqdm(input, desc="RETRIEVAL > "):
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

        if input:
            raise NotImplementedError

        elif self.isFrame and not ignoreFrame:
            raise NotImplementedError

        elif searchActive:
            pass

        resourcePageSize = 100
  
        self.client.resources 
        
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

                for element in tqdm(search, desc="SEARCH > ", total=resourceCount):
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

            result = fhirdrill.Drill().searchResources(
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
            result = self.prepareOutput(results, "binary")
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

    def getDICOMBytes(
        self,
        input: list[str] = None,
        operateOnCol: str = "data",
        resultInCol: str = None,
        params: dict = {},
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

        results = []

        for i, se, st in input[["series.uid", "study.uid"]].itertuples():
            try:
                for instance in tqdm(client.iter_series(st, se)):
                    newStudyInstanceUID = str(instance.StudyInstanceUID)
                    save_dir = (
                        f"moon/{newStudyInstanceUID}/{instance.SeriesDescription}"
                    )
                    os.makedirs(save_dir, exist_ok=True)
                    instance.save_as(f"{save_dir}/{instance.SOPInstanceUID}.dcm")
            except Exception as e:
                print(e)
                pass

            time.sleep(0.5)
        #     results.append(data)
        # if resultInCol:
        #     result = self.assign(**{resultInCol: results})
        # else:
        #     result = se
