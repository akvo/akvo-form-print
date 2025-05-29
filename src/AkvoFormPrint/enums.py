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
    SIGNATURE = "signature"


class AnswerFieldConfig(str, Enum):
    TEXTBOX = "textbox"
    OPTION_SINGLE_LINE = "option_single_line"


class HintText(str, Enum):
    OPTION = "Mark only one oval"
    MULTIPLE_OPTION = "Tick all that apply"
