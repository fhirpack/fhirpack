import json
from typing import Union

import requests

from fhirpy.lib import SyncFHIRResource
from fhirpy.lib import SyncFHIRReference

import fhirdrill.extraction.base as base


class ExtractorDiagnosticReportMixin(base.BaseExtractorMixin):
    def getDiagnosticReports(
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
            input = self.castOperand(input, SyncFHIRReference, "DiagnosticReport")
            result = self.getResources(input, resourceType="DiagnosticReport", raw=True)

        elif self.isFrame and not ignoreFrame:

            if self.resourceTypeIs("Patient"):
                input = self.data

                result = input.apply(
                    lambda x: self.searchResources(
                        searchParams=dict(searchParams, **{"subject": x.id}),
                        resourceType="DiagnosticReport",
                        raw=True,
                    )
                )
                result = result.values

            elif self.resourceTypeIs("DiagnosticReport"):
                input = self.data.values
                result = self.getResources(
                    input, resourceType="DiagnosticReport", raw=True
                )

            else:
                raise NotImplementedError

        elif searchActive:
            result = self.searchResources(
                searchParams=searchParams, resourceType="DiagnosticReport", raw=True
            )

        else:
            raise NotImplementedError

        result = self.prepareOutput(result, "DiagnosticReport")

        return result
