from fhirpack.load.patient import LoaderPatientMixin
from fhirpack.load.observation import LoaderObservationMixin
from fhirpack.load.condition import LoaderConditionMixin


class LoaderMixin(
    LoaderObservationMixin,
    LoaderPatientMixin,
    LoaderConditionMixin,
):

    # def __init__(self, client):
    # mixin methods should never have state of their own
    # otherwise the several levels of indirection make it
    # hard to understand the codebase
    # keep this class free of constructor, class variables
    # and similar
    pass
