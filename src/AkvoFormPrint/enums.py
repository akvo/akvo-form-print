from enum import Enum


class QuestionType(str, Enum):
    CASCADE = "cascade"
    GEO = "geo"
    INPUT = "input"
    NUMBER = "number"
    DATE = "date"
    OPTION = "option"
    MULTIPLE_OPTION = "multiple_option"
    IMAGE = "image"
    TEXT = "text"
    TABLE = "table"
    AUTOFIELD = "autofield"
    TREE = "tree"
