from fhirdrill.extraction.patient import ExtractorPatientMixin
from fhirdrill.extraction.observation import ExtractorObservationMixin
from fhirdrill.extraction.condition import ExtractorConditionMixin
from fhirdrill.extraction.diagnosticreport import ExtractorDiagnosticReportMixin
from fhirdrill.extraction.episodeofcare import ExtractorEpisodeOfCareMixin
from fhirdrill.extraction.familymemberhistory import ExtractorFamilyMemberHistoryMixin
from fhirdrill.extraction.imagingstudy import ExtractorImagingStudyMixin
from fhirdrill.extraction.medicationadministration import (
    ExtractorMedicationAdministrationMixin,
)
from fhirdrill.extraction.endpoint import ExtractorEndpointMixin

from fhirdrill.extraction.medicationrequest import ExtractorMedicationRequestMixin
from fhirdrill.extraction.list import ExtractorListMixin

# from fhirdrill.extraction. import Extractor Mixin


class ExtractorMixin(
    ExtractorObservationMixin,
    ExtractorPatientMixin,
    ExtractorConditionMixin,
    ExtractorDiagnosticReportMixin,
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
