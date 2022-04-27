from fhirdrill.config import Config

CONFIG = Config()

FHIR_NARRATIVE_ELEMENTS = [
    "display",
    "summary",
    "description",
    "title",
    "conclusion",
    # 'note',
    "text",
    #'answer',
    "valueString",
]

import json
from enum import Enum


class SampleEnum(Enum):
    sample = "sample"
