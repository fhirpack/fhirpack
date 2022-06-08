from fhirpack.extraction.patient import ExtractorPatientMixin
from fhirpack.extraction.observation import ExtractorObservationMixin
from fhirpack.extraction.condition import ExtractorConditionMixin
from fhirpack.extraction.diagnosticreport import ExtractorDiagnosticReportMixin
from fhirpack.extraction.episodeofcare import ExtractorEpisodeOfCareMixin
from fhirpack.extraction.encounter import ExtractorEncounterMixin
from fhirpack.extraction.familymemberhistory import ExtractorFamilyMemberHistoryMixin
from fhirpack.extraction.imagingstudy import ExtractorImagingStudyMixin
from fhirpack.extraction.medicationadministration import (
    ExtractorMedicationAdministrationMixin,
)
from fhirpack.extraction.endpoint import ExtractorEndpointMixin

from fhirpack.extraction.medicationrequest import ExtractorMedicationRequestMixin
from fhirpack.extraction.list import ExtractorListMixin

# from fhirpack.extraction. import Extractor Mixin


class ExtractorMixin(
    ExtractorObservationMixin,
    ExtractorPatientMixin,
    ExtractorConditionMixin,
    ExtractorDiagnosticReportMixin,
    ExtractorEncounterMixin,
    ExtractorEpisodeOfCareMixin,
    ExtractorFamilyMemberHistoryMixin,
    ExtractorMedicationRequestMixin,
    ExtractorMedicationAdministrationMixin,
    ExtractorListMixin,
    ExtractorImagingStudyMixin,
    ExtractorEndpointMixin,
    # Extractor Mixin,
):

    # def __init__(self, client):
    # mixin methods should never have state of their own
    # otherwise the several levels of indirection make it
    # hard to understand the codebase
    # keep this class free of constructor, class variables
    # and similar
    pass
