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

OPTION_TYPE = ["option", "multiple_option"]


class AkvoReactFormParser(BaseParser):
    def parse(self, raw_json: Dict[str, Any]) -> FormModel:
        form_title = raw_json.get("name", "Untitled Form")
        question_groups = raw_json.get("question_group", [])

        sections = []

        for group in question_groups:
            section_title = group.get("label", None) or group.get(
                "name", "Untitled Section"
            )

            questions_data = group.get("question", [])

            if isinstance(questions_data, dict):
                questions_data = [questions_data]

            questions: List[QuestionItem] = []

            for q in questions_data:
                q_type_raw = q.get("type", "input")
                q_id = q.get("id")
                q_text = q.get("label", None) or q.get("name", "Untitled Question")
                q_required = q.get("required", False)
                q_repeat = group.get("repeatable", False)
                q_variable_name = q.get("variableName", "")
                validation_rule = q.get("rule", None)

                max_val = None
                min_val = None
                number_box = 10
                if validation_rule:
                    max_val = validation_rule.get("max", None)
                    if max_val:
                        max_val = parse_int(max_val)
                        number_box = len(str(max_val))

                    min_val = validation_rule.get("min", None)
                    if min_val:
                        min_val = parse_int(min_val)

                # Option and Cascade Parsing
                options = []
                if q_type_raw in OPTION_TYPE:
                    option_data = q.get("option", [])
                    if isinstance(option_data, dict):
                        option_data = [option_data]
                    for option in option_data:
                        opt_value = option.get("label", None) or option.get(
                            "name", "Untitled Option"
                        )
                        options.append(opt_value)

                # TODO :: How to determine the levels
                elif q_type_raw == "cascade":
                    options = []

                # Handle dependency
                dependencies_data = q.get("dependency", [])
                dependencies = []

                if isinstance(dependencies_data, dict):
                    dependencies_data = [dependencies_data] if dependencies_data else []

                dependencies_data = dependencies_data if dependencies_data else []
                for dep in dependencies_data:
                    option_answer = dep.get("options", [])
                    min_answer = dep.get("min", None)
                    max_answer = dep.get("max", None)
                    not_equal_answer = dep.get("notEqual", None)
                    before_answer = dep.get("before", None)
                    after_answer = dep.get("after", None)

                    answer_value = None
                    if option_answer:
                        answer_value = ", ".join(option_answer)
                    if min_answer or min_answer == 0:
                        answer_value = f"min: ${min_answer}"
                    if max_answer or max_answer == 0:
                        answer_value = f"max: ${max_answer}"
                    if not_equal_answer or not_equal_answer == 0:
                        answer_value = f"min: ${not_equal_answer}"
                    if before_answer:
                        answer_value = f"before: ${before_answer}"
                    if after_answer:
                        answer_value = f"before: ${after_answer}"

                    dependencies.append(
                        QuestionDependency(
                            depends_on_question_id=dep.get("id"),
                            expected_answer=answer_value,
                        )
                    )

                # Decide final question type
                mapped_type = self._map_question_type(q_type_raw, q)
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
                        q.get("allowOther", False)
                        if q_type_raw in OPTION_TYPE
                        else False
                    ),
                    numberBox=number_box,
                    optionSingleLine=(
                        True
                        if q_variable_name == AnswerFieldConfig.OPTION_SINGLE_LINE
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

            sections.append(FormSection(title=section_title, questions=questions))

        return FormModel(title=form_title, sections=sections)

    def _map_question_type(self, q_type: str, q_data: Dict[str, Any]) -> QuestionType:
        mapping = {
            "cascade": QuestionType.CASCADE,
            "geo": QuestionType.GEO,
            "input": QuestionType.INPUT,
            "number": QuestionType.NUMBER,
            "date": QuestionType.DATE,
            "option": QuestionType.OPTION,
            "multiple_option": QuestionType.MULTIPLE_OPTION,
            "image": QuestionType.IMAGE,
            "text": QuestionType.TEXT,
            "table": QuestionType.TABLE,
            "autofield": QuestionType.AUTOFIELD,
            "tree": QuestionType.TREE,
            "signature": QuestionType.SIGNATURE,
        }
        return mapping.get(q_type, QuestionType.INPUT)

    def _map_variable_name_type(
        self, q_type: QuestionType, variable_name: Optional[str]
    ) -> Optional[QuestionType]:
        if q_type == QuestionType.INPUT and variable_name:
            if variable_name.strip().lower() == AnswerFieldConfig.TEXTBOX:
                return QuestionType.TEXT
        return None
