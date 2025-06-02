from typing import Any, Dict, List, Optional
from AkvoFormPrint.models import (
    FormModel,
    FormSection,
    QuestionItem,
    AnswerField,
    QuestionDependency,
)
from AkvoFormPrint.parsers.base_parser import BaseParser
from AkvoFormPrint.enums import QuestionType, AnswerFieldConfig
from AkvoFormPrint.utils import parse_int


class AkvoFlowFormParser(BaseParser):
    def parse(self, raw_json: Dict[str, Any]) -> FormModel:
        form_title = raw_json.get("name", "Untitled Form")
        question_groups = raw_json.get("questionGroup", [])

        sections = []

        for group in question_groups:
            section_title = group.get("heading", "Untitled Section")
            questions_data = group.get("question", [])

            if isinstance(questions_data, dict):
                questions_data = [questions_data]

            questions: List[QuestionItem] = []

            for q in questions_data:
                q_type_raw = q.get("type", "free")
                q_id = q.get("id")
                q_text = q.get("text", "Untitled Question")
                q_required = q.get("mandatory", False)
                q_repeat = group.get("repeatable", False)
                q_variable_name = q.get("variableName", "")
                validation_rule = q.get("validationRule", {})
                max_val = validation_rule.get("maxVal", None)
                number_box = 10
                if max_val:
                    max_val = parse_int(max_val)
                    number_box = len(str(max_val))

                min_val = validation_rule.get("minVal", None)
                if min_val:
                    min_val = parse_int(min_val)

                # Option and Cascade Parsing
                options = []
                if q_type_raw == "option":
                    option_data = q.get("options", {}).get("option", [])
                    if isinstance(option_data, dict):
                        option_data = [option_data]
                    options = [
                        opt["text"] for opt in option_data if "text" in opt
                    ]

                elif q_type_raw == "cascade":
                    levels = q.get("levels", {}).get("level", [])
                    if isinstance(levels, dict):
                        levels = [levels]
                    options = [
                        level.get("text", "")
                        for level in levels
                        if "text" in level
                    ]

                # Handle dependency
                dependencies_data = q.get("dependency", [])
                dependencies = []

                if isinstance(dependencies_data, dict):
                    dependencies_data = (
                        [dependencies_data] if dependencies_data else []
                    )

                for dep in dependencies_data:
                    # Handle both answer-value and answerValue formats
                    answer_value = dep.get("answer-value")
                    if answer_value is None:
                        # Try answerValue format which can be a list
                        answer_value = dep.get("answerValue")
                        if isinstance(answer_value, list):
                            answer_value = ", ".join(answer_value)

                    dependencies.append(
                        QuestionDependency(
                            depends_on_question_id=dep.get("question"),
                            expected_answer=answer_value,
                        )
                    )

                # Decide final question type
                mapped_type = self._map_question_type(q_type_raw, q)
                mapped_type = self._map_validation_rule(
                    mapped_type, validation_rule
                )
                override_type = self._map_variable_name_type(
                    mapped_type, q_variable_name
                )
                final_type = override_type or mapped_type

                # Build answer
                answer_field = AnswerField(
                    id=q_id,
                    type=final_type,
                    required=q_required,
                    options=options if options else [],
                    repeat=q_repeat,
                    allowOther=(
                        q.get("options", {}).get("allowOther", False)
                        if q_type_raw == "option"
                        else False
                    ),
                    numberBox=number_box,
                    optionSingleLine=(
                        True
                        if q_variable_name
                        == AnswerFieldConfig.OPTION_SINGLE_LINE
                        else False
                    ),
                    maxValue=max_val,
                    minValue=min_val,
                )

                question = QuestionItem(
                    id=q_id,
                    label=q_text,
                    type=final_type,
                    answer=answer_field,
                    dependencies=dependencies or [],
                )

                questions.append(question)

            sections.append(
                FormSection(title=section_title, questions=questions)
            )

        return FormModel(title=form_title, sections=sections)

    def _map_question_type(
        self, q_type: str, q_data: Dict[str, Any]
    ) -> QuestionType:
        if q_type == "option":
            allow_multiple = q_data.get("options", {}).get(
                "allowMultiple", False
            )
            return (
                QuestionType.MULTIPLE_OPTION
                if allow_multiple
                else QuestionType.OPTION
            )

        mapping = {
            "free": QuestionType.INPUT,
            "date": QuestionType.DATE,
            "cascade": QuestionType.CASCADE,
            "photo": QuestionType.IMAGE,
            "video": QuestionType.IMAGE,
            "signature": QuestionType.SIGNATURE,
            "geo": QuestionType.GEO,
        }
        return mapping.get(q_type, QuestionType.INPUT)

    def _map_validation_rule(
        self, q_type: QuestionType, validation_rule: Optional[dict] = {}
    ) -> QuestionType:
        if q_type == QuestionType.INPUT:
            if validation_rule.get("validationType") == "numeric":
                return QuestionType.NUMBER
        return q_type

    def _map_variable_name_type(
        self, q_type: QuestionType, variable_name: Optional[str]
    ) -> Optional[QuestionType]:
        if q_type == QuestionType.INPUT and variable_name:
            if variable_name.strip().lower() == AnswerFieldConfig.TEXTBOX:
                return QuestionType.TEXT
        return None
