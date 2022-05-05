import json
import importlib
from typing import Union

import pandas as pd

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference

import fhirpack.base as base
import fhirpack.custom.extraction.base as cumextbase
import fhirpack.utils as utils


class PluginSHIPExtractorMixin(cumextbase.PluginBaseExtractorMixin):
    def getDiagnosticReportsSHIP(
        self,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        searchParams: dict = None,
        params: dict = None,
        ignoreFrame: bool = False,
    ):

        searchActive = False if searchParams is None else True
        searchParams = {} if searchParams is None else searchParams
        params = {} if params is None else params
        input = [] if input is None else input
        result = []

        paths = [
            "id",
            # "conclusion",
            "subject.reference",
            "presentedForm.contentType",
            "presentedForm.url",
            "presentedForm.title",
            "presentedForm.creation",
        ]

        if len(input):
            raise NotImplementedError

        elif self.isFrame and not ignoreFrame:

            result = self.getDiagnosticReports(
                input=input,
                searchParams=searchParams,
                params=params,
                ignoreFrame=ignoreFrame,
            ).explode("data")
            result = result.gatherSimplePaths(paths)

        elif searchActive:
            raise NotImplementedError

        else:
            raise NotImplementedError

        return result

    def getDiagnosticReportsFilesSHIP(
        self,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        searchParams: dict = None,
        params: dict = None,
        ignoreFrame: bool = False,
    ):

        searchActive = False if searchParams is None else True
        searchParams = {} if searchParams is None else searchParams
        params = {} if params is None else params
        input = [] if input is None else input
        result = []

        paths = [
            "id",
            # "conclusion",
            "subject.reference",
            "presentedForm.contentType",
            "presentedForm.url",
            "presentedForm.title",
            "presentedForm.creation",
        ]

        if len(input):
            raise NotImplementedError

        elif self.isFrame and not ignoreFrame:

            input = self
            input["path"] = (
                input["id"]
                + "_"
                + input["presentedForm.url"].str.split("/").str[-1:].str[0]
            )
            input["data"] = input.getURLBytes(operateOnCol="presentedForm.url")

            result = input.sendBytesToFile()

        elif searchActive:
            raise NotImplementedError

        else:
            raise NotImplementedError

        return result

    def getTumorIdsSHIP(
        self,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        searchParams: dict = None,
        params: dict = None,
        ignoreFrame: bool = False,
    ):

        searchActive = False if searchParams is None else True
        searchParams = {} if searchParams is None else searchParams
        params = {} if params is None else params
        input = [] if input is None else input
        result = []

        if len(input):
            raise NotImplementedError

        elif self.isFrame and not ignoreFrame:

            input = self

            if self.resourceTypeIs("Patient"):
                input = self

                searchParams.update(
                    {
                        "identifier": "https://uk-essen.de/HIS/Cerner/Medico/EpisodeOfCare/TumorDocumentation|"
                    }
                )

                input.data = input.data.apply(
                    lambda x: self.searchResources(
                        searchParams=dict(searchParams, **{"patient": x.id}),
                        resourceType="EpisodeOfCare",
                        raw=True,
                    )
                )
                result = input.gatherSimplePaths(["identifier.value"]).rename(
                    columns={"identifier.value": "data"}
                )
                result = result.data.dropna().apply(utils.flattenList).explode()
                result = result.unique()

            else:
                raise NotImplementedError

        elif searchActive:
            raise NotImplementedError

        else:
            raise NotImplementedError

        result = self.prepareOutput(result, "EpisodeOfCare")
        return result

    def getTumorReferencesSHIP(
        self,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        params: dict = None,
        ignoreFrame: bool = False,
        searchParams: dict = None,
    ):
        searchActive = False if searchParams is None else True
        searchParams = {} if searchParams is None else searchParams
        params = {} if params is None else params
        input = [] if input is None else input
        result = []

        if len(input):
            pass
        elif self.isFrame and not ignoreFrame:
            if self.resourceTypeIs("EpisodeOfCare"):
                input = self

                input["identifier"] = input.data.apply(
                    lambda x: {
                        "identifier": "https://uk-essen.de/HIS/Cerner/Medico/TumorDocumentation|"
                        + x
                    }
                )

                input.data = input.identifier.apply(
                    lambda x: self.searchResources(
                        searchParams=dict(searchParams, **x),
                        resourceType="List",
                        raw=True,
                    )
                )
                input.data = input.data.explode()
                result = input.gatherSimplePaths(["entry.item.reference"]).rename(
                    columns={"entry.item.reference": "data"}
                )

        elif searchActive:
            raise NotImplementedError

        # result = self.prepareOutput(result, "Mixed")
        self.setResourceType("Invalid")

        return result

    # def getTumorBoardQuestions(
    #     self,
    #     patient: Union[str, fhirpy.lib.SyncFHIRReference, fhirpy.lib.SyncFHIRResource],
    #     includeLinkedPatients: bool = False,
    #     params: dict = None,
    # ):
    #     """_summary_"""
    #     params = {} if params is None else params

    #     patientType = type(patient)

    #     if patientType is str:
    #         patient = self.client.reference("Patient", patient)
    #     elif patientType is fhirpy.lib.SyncFHIRReference:
    #         if patient.resource_type == "Patient":
    #             pass
    #         else:
    #             raise Exception("patient reference must be of type Patient")
    #     elif patientType is fhirpy.lib.SyncFHIRResource:
    #         if patient.resource_type == "Patient":
    #             pass
    #         else:
    #             raise Exception("patient resource must be of type Patient")

    #     patientsOfInterest = []
    #     if includeLinkedPatients:
    #         patientsOfInterest = [patient] + self.getLinkedPatients(patient)
    #     else:
    #         patientsOfInterest = [patient]

    #     return None

    # # TODO:
    # def getTumorBoardRecommendations(
    #     self,
    #     patient: Union[str, fhirpy.lib.SyncFHIRReference, fhirpy.lib.SyncFHIRResource],
    #     includeLinkedPatients: bool = False,
    #     params: dict = None,
    # ):
    #     """_summary_"""
    #     params = {} if params is None else params

    #     patientType = type(patient)

    #     if patientType is str:
    #         patient = self.client.reference("Patient", patient)
    #     elif patientType is fhirpy.lib.SyncFHIRReference:
    #         if patient.resource_type == "Patient":
    #             pass
    #         else:
    #             raise Exception("patient reference must be of type Patient")
    #     elif patientType is fhirpy.lib.SyncFHIRResource:
    #         if patient.resource_type == "Patient":
    #             pass
    #         else:
    #             raise Exception("patient resource must be of type Patient")

    #     patientsOfInterest = []
    #     if includeLinkedPatients:
    #         patientsOfInterest = [patient] + self.getLinkedPatients(patient)
    #     else:
    #         patientsOfInterest = [patient]

    #     return None
