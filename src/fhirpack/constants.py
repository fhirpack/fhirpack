from enum import Enum
import json
from fhirpack.config import Config

CONFIG = Config()

FHIR_NARRATIVE_ELEMENTS = [
    "display",
    "summary",
    "description",
    "title",
    "conclusion",
    # 'note',
    "text",
    # 'answer',
    "valueString",
]


class SampleEnum(Enum):
    sample = "sample"
