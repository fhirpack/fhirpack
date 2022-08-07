from typing import Union

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference

from tqdm import tqdm
import pandas as pd

import fhirpack.utils as utils
import fhirpack.base as base
import fhirpack.extraction.base as extractionBase


class ExtractorPatientMixin(extractionBase.BaseExtractorMixin):

    # TODO test len(references) = 0
    # TODO test len(references) = 1
    # TODO test len(references) > 1
    # TODO raise len(references) = 0?

    def getPatients(
        self,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        searchParams: dict = None,
        params: dict = None,
        ignoreFrame: bool = False,
        *args,
        **kwargs,
    ):

        return self.getResources(
            input=input,
            searchParams=searchParams,
            params=params,
            ignoreFrame=ignoreFrame,
            resourceType="Patient",
            *args,
            **kwargs,
        )

    # TODO test len(result) = 0
    # TODO test len(result) = 1
    # TODO test len(result) > 1
    # TODO raise len(result) > 1

    def getRootPatients(
        self,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        searchParams: dict = None,
        params: dict = None,
        ignoreFrame: bool = False,
        raw: bool = False,
    ):

        searchActive = False if searchParams is None else searchParams
        searchParams = {} if searchParams is None else searchParams
        params = {} if params is None else params
        input = [] if input is None else input
        result = []

        if len(input):
            return self.getPatients(input).getRootPatients()

        elif self.isFrame and not ignoreFrame:
            input = self
            if input.resourceType in ["Patient", "LinkedPatient"]:

                result = input.getResources(
                    resourceType="Patient",
                    metaResourceType="RootPatient",
                    raw=True,
                )

                result = self.prepareOutput(result, "RootPatient")
                input, result = self.attachOperandIds(input, result, "RootPatient")

                # return input when no root patients exist
                result = pd.merge(
                    result,
                    input,
                    on=self.resourceType,  # 'Patient',
                    suffixes=["", "_self"],
                    how="right",
                )
                result["data"] = result["data"].mask(
                    result["data"].isna(), result["data_self"]
                )
                result[result.resourceType] = result[result.resourceType].mask(
                    result[result.resourceType].isna(), result[self.resourceType]
                )
                result.drop(columns=["data_self"], inplace=True)
            else:
                raise NotImplementedError

        elif searchActive:
            raise NotImplementedError
        else:
            raise NotImplementedError

        return result

    def getLinkedPatients(
        self,
        input: Union[
            list[str],
            list[SyncFHIRReference],
            list[SyncFHIRResource],
        ] = None,
        searchParams: dict = None,
        params: dict = None,
        ignoreFrame: bool = False,
        raw: bool = False,
    ):

        searchActive = False if searchParams is None else searchParams
        searchParams = {} if searchParams is None else searchParams
        params = {} if params is None else params
        input = [] if input is None else input
        result = []

        if len(input):
            return self.getPatients(input).getLinkedPatients()

        elif self.isFrame and not ignoreFrame:
            input = self

            if input.resourceTypeIs("Patient"):
                return input.getRootPatients().getLinkedPatients()

            elif input.resourceTypeIs("RootPatient"):

                result = self.getResources(
                    resourceType="Patient",
                    metaResourceType="LinkedPatient",
                    raw=True,
                )

                result = self.prepareOutput(result, "LinkedPatient")
                input, result = self.attachOperandIds(self, result, "LinkedPatient")

                # return input when no linked patients exist
                result = pd.merge(
                    result,
                    input,
                    on=result.resourceType,
                    suffixes=["", "_self"],
                    how="right",
                )
                result["data"] = result["data"].mask(
                    result["data"].isna(), result["data_self"]
                )
                result["Patient"] = result["Patient"].mask(
                    result["Patient"].isna(), result["Patient_self"]
                )

                result[input.resourceType] = result[input.resourceType].mask(
                    result[input.resourceType].isna(),
                    result[f"{input.resourceType}_self"],
                )
                result[result.resourceType] = result[result.resourceType].mask(
                    result[result.resourceType].isna(),
                    result[f"{input.resourceType}_self"],
                )

                toDrop = [e for e in result.columns if e.endswith("_self")]
                result.drop(columns=toDrop, inplace=True)

            else:
                raise NotImplementedError
        elif searchActive:
            raise NotImplementedError
        else:
            raise NotImplementedError

        return result
