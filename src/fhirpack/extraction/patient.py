from typing import Union

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference

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
            # list[SyncFHIRResource],
        ] = None,
        searchParams: dict = None,
        includeLinkedPatients=False,
        params: dict = None,
        ignoreFrame: bool = False,
    ):

        if includeLinkedPatients:
            return self.getLinkedPatients(input, searchParams)

        searchActive = False if searchParams is None else True
        searchParams = {} if searchParams is None else searchParams
        params = {} if params is None else params
        input = [] if input is None else input
        result = []

        if len(input):
            input = self.castOperand(input, SyncFHIRReference, "Patient")
            result = self.getResources(input, resourceType="Patient", raw=True)

        elif self.isFrame and not ignoreFrame:

            utils.validateFrame(self)

            input = self.data

            if self.resourceTypeIs("Condition"):

                result = input.apply(
                    lambda x: self.searchResources(
                        searchParams=dict(searchParams, **{"_id": x.subject.id}),
                        resourceType="Patient",
                        raw=True,
                    )
                )
            elif self.resourceTypeIs("Patient"):
                result = input.apply(
                    lambda x: self.searchResources(
                        searchParams=dict(searchParams, **{"_id": x.id}),
                        resourceType="Patient",
                        raw=True,
                    )
                )
            elif self.resourceTypeIs("DiagnosticReport"):
                result = input.apply(
                    lambda x: self.searchResources(
                        searchParams=dict(searchParams, **{"_id": x.subject.id}),
                        resourceType="Patient",
                        raw=True,
                    )
                )
            elif self.resourceTypeIs("ImagingStudy"):
                result = input.apply(
                    lambda x: self.searchResources(
                        searchParams=dict(searchParams, **{"_id": x.subject.id}),
                        resourceType="Patient",
                        raw=True,
                    )
                )
            else:
                raise NotImplementedError

            result = result.values

        elif searchActive:
            result = self.searchResources(
                searchParams=searchParams, resourceType="Patient", raw=True
            )

        else:
            raise NotImplementedError

        result = self.prepareOutput(result)

        return result

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
    ):

        searchActive = False if searchParams is None else searchParams
        searchParams = {} if searchParams is None else searchParams
        params = {} if params is None else params
        input = [] if input is None else input
        result = []

        if len(input):
            pass
        elif self.isFrame and not ignoreFrame:
            input = self
        elif searchActive:
            raise NotImplementedError
        else:
            raise NotImplementedError

        input = self.castOperand(input, SyncFHIRResource, "Patient")
        input = self.castOperand(input, base.Frame, "Patient")

        if input.resourceTypeIs("Patient"):
            input = input.data

            result = input.apply(
                lambda x: self.searchResources(
                    searchParams=dict(searchParams, **{"link": x.id}),
                    resourceType="Patient",
                    raw=True,
                )
            )

            result = result.combine(input, lambda x, y: x if len(x) > 0 else [y])

        else:
            raise NotImplementedError

        result = self.prepareOutput(result, "Patient")

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
    ):

        searchActive = False if searchParams is None else searchParams
        searchParams = {} if searchParams is None else searchParams
        params = {} if params is None else params
        input = [] if input is None else input
        result = []

        if len(input):
            pass

        elif self.isFrame and not ignoreFrame:
            input = self

        elif searchActive:
            raise NotImplementedError

        else:
            raise NotImplementedError

        input = self.castOperand(input, SyncFHIRReference, "Patient")
        input = self.castOperand(input, base.Frame, "Patient")

        if input.resourceTypeIs("Patient"):

            rootPatients = input.getRootPatients().explode("data", ignore_index=True)

            input = rootPatients.gatherSimplePaths(["link.other.reference"]).rename(
                columns={"link.other.reference": "data"}
            )
            # .fillna("").apply(list)

            patients = input.data.apply(
                lambda x: self.getResources(
                    x, ignoreFrame=True, resourceType="Patient"
                ).data.values,
            )

            result = patients

        else:
            raise NotImplementedError

        result = self.prepareOutput(result, "Patient")

        if not result.size:
            result = input

        return result
