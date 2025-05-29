from typing import List, Optional, Union
from pydantic import BaseModel
from .enums import QuestionType


class AnswerField(BaseModel):
    id: Union[str, int]
    type: QuestionType
    required: bool = False
    options: Optional[List[str]] = []
    repeat: Optional[bool] = False
    allowOther: Optional[bool] = False


class QuestionItem(BaseModel):
    id: Union[str, int]
    label: str
    type: QuestionType
    answer: AnswerField
    number: Optional[int] = None


class FormSection(BaseModel):
    title: str
    questions: List[QuestionItem]


class FormModel(BaseModel):
    title: str
    sections: List[FormSection]
