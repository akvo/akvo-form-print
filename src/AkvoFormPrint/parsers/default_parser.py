from typing import Any, Dict
from AkvoFormPrint.models import (
    FormModel,
    FormSection,
    QuestionItem,
    AnswerField,
    QuestionDependency,
)
from AkvoFormPrint.enums import QuestionType
from .base_parser import BaseParser


class DefaultParser(BaseParser):
    def parse(self, raw_input: Dict[str, Any]) -> FormModel:
        """Parse the default form JSON format into a FormModel."""
        title = raw_input["title"]
        sections = []

        for section in raw_input["sections"]:
            questions = []
            for question in section["questions"]:
                # Create answer field
                answer = AnswerField(
                    id=question["id"],
                    type=self._parse_question_type(question["type"]),
                    required=question.get("required", False),
                    options=question.get("options", []),
                    allowOther=question.get("allowOther", False),
                    optionSingleLine=question.get("optionSingleLine", False),
                    minValue=question.get("minValue"),
                    maxValue=question.get("maxValue"),
                )

                # Create dependencies if they exist
                dependencies = None
                if "dependencies" in question:
                    dependencies = [
                        QuestionDependency(
                            depends_on_question_id=dep["depends_on_question_id"],
                            expected_answer=dep["expected_answer"],
                        )
                        for dep in question["dependencies"]
                    ]

                # Create question item
                question_item = QuestionItem(
                    id=question["id"],
                    label=question["label"],
                    type=self._parse_question_type(question["type"]),
                    answer=answer,
                    hint=question.get("hint"),
                    dependencies=dependencies,
                )
                questions.append(question_item)

            section_model = FormSection(
                title=section["title"],
                questions=questions,
            )
            sections.append(section_model)

        return FormModel(title=title, sections=sections)

    def _parse_question_type(self, type_str: str) -> QuestionType:
        """Convert string type to QuestionType enum."""
        type_mapping = {
            "input": QuestionType.INPUT,
            "number": QuestionType.NUMBER,
            "text": QuestionType.TEXT,
            "date": QuestionType.DATE,
            "option": QuestionType.OPTION,
            "multiple_option": QuestionType.MULTIPLE_OPTION,
            "image": QuestionType.IMAGE,
            "photo": QuestionType.IMAGE,  # map photo to image type
            "geo": QuestionType.GEO,
            "cascade": QuestionType.CASCADE,
            "table": QuestionType.TABLE,
            "autofield": QuestionType.AUTOFIELD,
            "tree": QuestionType.TREE,
            "signature": QuestionType.SIGNATURE,
        }
        return type_mapping.get(type_str.lower(), QuestionType.INPUT)
