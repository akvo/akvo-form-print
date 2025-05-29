from typing import List, Optional, Union
from pydantic import BaseModel, root_validator
from .enums import QuestionType, HintText

# TODO :: create akvo react form parser


class AnswerField(BaseModel):
    id: Union[str, int]
    type: QuestionType
    required: bool = False
    options: Optional[List[str]] = []
    repeat: Optional[bool] = False
    allowOther: Optional[bool] = False
    numberBox: Optional[int] = 10
    optionSingleLine: Optional[bool] = False


class QuestionItem(BaseModel):
    id: Union[str, int]
    label: str
    type: QuestionType
    answer: AnswerField
    number: Optional[int] = None  # for question number (increment)
    hint: Optional[str] = None

    @root_validator(pre=True)
    def set_hint_by_type(cls, values):
        if "hint" not in values or values["hint"] is None:
            qtype = values.get("type")
            if qtype == QuestionType.OPTION:
                values["hint"] = HintText.OPTION
            elif qtype == QuestionType.MULTIPLE_OPTION:
                values["hint"] = HintText.MULTIPLE_OPTION
            else:
                values["hint"] = None
        return values


class FormSection(BaseModel):
    title: str
    questions: List[QuestionItem]


class FormModel(BaseModel):
    title: str
    sections: List[FormSection]
