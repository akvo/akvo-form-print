from enum import Enum


class QuestionType(str, Enum):
    TEXT = "text"
    TEXTAREA = "textarea"
    NUMBER = "number"
    SELECT = "select"
    DATE = "date"
    CASCADE = "cascade"
    FILE = "file"
    SIGNATURE = "signature"
    GEOLOCATION = "geolocation"
