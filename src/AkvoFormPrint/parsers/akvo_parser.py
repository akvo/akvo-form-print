from typing import Any, Dict, List, Optional
from AkvoFormPrint.models import (
    FormModel,
    FormSection,
    QuestionItem,
    AnswerField,
)
from AkvoFormPrint.parsers.base_parser import BaseParser
from AkvoFormPrint.enums import QuestionType


class AkvoFormParser(BaseParser):
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
                q_type = q.get("type", "free")
                q_id = q.get("id")
                q_text = q.get("text", "Untitled Question")
                q_required = q.get("mandatory", False)
                q_repeat = group.get("repeatable", False)
                q_variable_name = q.get("variableName", "")
                validation_rule = q.get("validationRule", {})

                options = []
                allowOther = False
                allowMultiple = False

                if q_type == "option" and "options" in q:
                    option_data = q["options"].get("option", [])
                    if isinstance(option_data, dict):
                        option_data = [option_data]

                    options = [
                        opt["text"] for opt in option_data if "text" in opt
                    ]

                    options_obj = q.get("options", {})
                    allowMultiple = options_obj.get("allowMultiple", False)
                    allowOther = options_obj.get("allowOther", False)

                elif q_type == "cascade":
                    levels = q.get("levels", {}).get("level", [])
                    if isinstance(levels, dict):
                        levels = [levels]

                    options = [
                        level.get("text", "")
                        for level in levels
                        if "text" in level
                    ]

                # Map initial type
                mapped_type = self._map_question_type(q_type)
                # Override based on validationRule
                mapped_type = self._map_validation_rule(
                    mapped_type, validation_rule
                )
                # Override based on variableName (only if not None)
                override_type = self._map_variable_name_type(
                    mapped_type, q_variable_name
                )
                final_type = (
                    override_type if override_type is not None else mapped_type
                )

                answer_field = AnswerField(
                    id=q_id,
                    type=final_type,
                    required=q_required,
                    options=options if options else None,
                    repeat=q_repeat,
                    allowOther=allowOther,
                    allowMultiple=allowMultiple,
                )

                question = QuestionItem(
                    id=q_id,
                    label=q_text,
                    type=final_type,
                    answer=answer_field,
                )

                questions.append(question)

            sections.append(
                FormSection(title=section_title, questions=questions)
            )

        return FormModel(title=form_title, sections=sections)

    def _map_question_type(self, q_type: str) -> QuestionType:
        mapping = {
            "free": QuestionType.TEXT,
            "option": QuestionType.SELECT,
            "date": QuestionType.DATE,
            "cascade": QuestionType.CASCADE,
            "photo": QuestionType.FILE,
            "video": QuestionType.FILE,
            "signature": QuestionType.SIGNATURE,
            "geo": QuestionType.GEOLOCATION,
        }
        return mapping.get(q_type, QuestionType.TEXT)

    def _map_validation_rule(
        self, q_type: str, validation_rule: Optional[dict] = {}
    ) -> QuestionType:
        """
        RUN: _map_question_type first before use this fn
        """
        if q_type == QuestionType.TEXT:
            isNumeric = validation_rule.get("validationType", None)
            if isNumeric:
                return QuestionType.NUMBER
        return q_type

    def _map_variable_name_type(
        self, q_type: str, variable_name: Optional[str]
    ) -> Optional[QuestionType]:
        """
        RUN: _map_question_type first before use this fn
        Custom mapping from variableName to QuestionType if applicable.
        Only applies for specific q_type values (like "free").
        """
        if q_type == QuestionType.TEXT:
            variable_mapping = {
                "textbox": QuestionType.TEXTAREA,
                # future mappings can go here
            }
            if variable_name:
                return variable_mapping.get(variable_name.strip().lower())
        # future mappings can go here
        return None
