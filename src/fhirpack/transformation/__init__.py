from fhirpack.transformation.patient import TransformerPatientMixin
from fhirpack.transformation.observation import TransformerObservationMixin
from fhirpack.transformation.condition import TransformerConditionMixin

# from fhirpack.transformation. import Transformer Mixin


class TransformerMixin(
    TransformerObservationMixin,
    TransformerPatientMixin,
    TransformerConditionMixin,
    # Transformer Mixin,
):

    # def __init__(self, client):
    # mixin methods should never have state of their own
    # otherwise the several levels of indirection make it
    # hard to understand the codebase
    # keep this class free of constructor, class variables
    # and similar
    pass
