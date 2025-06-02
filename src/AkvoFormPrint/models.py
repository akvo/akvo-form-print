from typing import List, Optional, Union
from pydantic import BaseModel, model_validator
from .enums import QuestionType, HintText
from collections import defaultdict


class QuestionDependency(BaseModel):
    depends_on_question_id: Union[str, int]
    expected_answer: str


class AnswerField(BaseModel):
    id: Union[str, int]
    type: QuestionType
    required: bool = False
    options: Optional[List[str]] = []
    repeat: Optional[bool] = False
    allowOther: Optional[bool] = False
    numberBox: Optional[int] = 10
    optionSingleLine: Optional[bool] = False
    minValue: Optional[int] = None
    maxValue: Optional[int] = None


class QuestionItem(BaseModel):
    id: Union[str, int]
    label: str
    type: QuestionType
    answer: AnswerField
    number: Optional[int] = None  # for question number (increment)
    hint: Optional[str] = None
    dependencies: Optional[List[QuestionDependency]] = []

    @model_validator(mode="before")
    @classmethod
    def set_hint_by_type(cls, values):
        if not isinstance(values, dict):
            return values

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
    letter: Optional[str] = None  # for section number A, B, C ...


class FormModel(BaseModel):
    title: str
    sections: List[FormSection]

    @property
    def question_id_to_info(self) -> dict[str, tuple[str, str]]:
        question_map = {}
        for section in self.sections:
            for question in section.questions:
                if section.letter and question.number:
                    question_code = f"{section.letter}.{question.number}"
                elif question.number:
                    question_code = str(question.number)
                else:
                    question_code = ""
                question_map[str(question.id)] = (
                    question_code,
                    question.label,
                )
        return question_map

    @property
    def question_reverse_dependency_map(
        self,
    ) -> dict[str, list[tuple[str, QuestionItem]]]:
        reverse_map = defaultdict(list)
        for section in self.sections:
            for question in section.questions:
                if hasattr(question, "dependencies") and question.dependencies:
                    for dep in question.dependencies:
                        key = str(dep.depends_on_question_id)
                        if section.letter and question.number:
                            question_code = f"{section.letter}.{question.number}"
                        elif question.number:
                            question_code = str(question.number)
                        else:
                            question_code = str(question.id)

                        reverse_map[key].append((question_code, question))
        return reverse_map

    @model_validator(mode="before")
    @classmethod
    def validate_question_dependencies(cls, values):
        if not isinstance(values, dict):
            return values

        questions = values.get("questions", [])
        dependency_map = {}

        for question in questions:
            if question.get("dependency") is not None:
                dependency = question["dependency"]
                if dependency not in dependency_map:
                    dependency_map[dependency] = []
                dependency_map[dependency].append(question["id"])

        values["question_dependency_map"] = dependency_map
        return values
