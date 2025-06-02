import pytest
from AkvoFormPrint.parsers.akvo_arf_parser import AkvoReactFormParser
from AkvoFormPrint.enums import QuestionType
from AkvoFormPrint.models import FormModel


@pytest.fixture
def raw_form_json():
    return {
        "name": "ARF Sample Form",
        "question_group": [
            {
                "name": "Personal Info",
                "order": 1,
                "question": [
                    {
                        "id": "q1",
                        "name": "full_name",
                        "type": "input",
                        "label": "Full Name",
                        "required": True,
                        "meta": False,
                    },
                    {
                        "id": "q2",
                        "name": "age",
                        "type": "number",
                        "label": "Age",
                        "required": True,
                        "meta": False,
                        "rule": {"min": 0, "max": 120},
                    },
                    {
                        "id": "q3",
                        "name": "interests",
                        "type": "multiple_option",
                        "label": "Select your interests",
                        "required": False,
                        "meta": False,
                        "option": [
                            {"label": "Reading", "value": "reading"},
                            {"label": "Sports", "value": "sports"},
                            {"label": "Music", "value": "music"},
                        ],
                        "allowOther": True,
                    },
                    {
                        "id": "q4",
                        "name": "other_interests",
                        "type": "input",
                        "label": "Specify other interests",
                        "required": False,
                        "meta": False,
                        "dependency": [{"id": "q3", "options": ["other"]}],
                    },
                ],
            }
        ],
    }


def test_parser_generates_correct_form_model(raw_form_json):
    parser = AkvoReactFormParser()
    result: FormModel = parser.parse(raw_form_json)

    assert result.title == "ARF Sample Form"
    assert len(result.sections) == 1

    section = result.sections[0]
    assert section.title == "Personal Info"
    assert len(section.questions) == 4

    # Test text question
    q1 = section.questions[0]
    assert q1.id == "q1"
    assert q1.type == QuestionType.INPUT
    assert q1.label == "Full Name"
    assert q1.answer.required is True

    # Test number question with min/max
    q2 = section.questions[1]
    assert q2.type == QuestionType.NUMBER
    assert q2.answer.minValue == 0
    assert q2.answer.maxValue == 120

    # Test multiple choice question
    q3 = section.questions[2]
    assert q3.type == QuestionType.MULTIPLE_OPTION
    assert len(q3.answer.options) == 3
    assert q3.answer.options == ["Reading", "Sports", "Music"]
    assert q3.answer.allowOther is True

    # Test dependency
    q4 = section.questions[3]
    assert q4.type == QuestionType.INPUT
    assert len(q4.dependencies) == 1
    assert q4.dependencies[0].depends_on_question_id == "q3"
    assert q4.dependencies[0].expected_answer == "other"


def test_parser_handles_all_arf_question_types():
    form_json = {
        "name": "All Types Form",
        "question_group": [
            {
                "name": "All Types",
                "order": 1,
                "question": [
                    {
                        "id": "q1",
                        "type": "input",
                        "label": "Text",
                        "name": "text",
                    },
                    {
                        "id": "q2",
                        "type": "number",
                        "label": "Number",
                        "name": "number",
                    },
                    {
                        "id": "q3",
                        "type": "date",
                        "label": "Date",
                        "name": "date",
                    },
                    {
                        "id": "q4",
                        "type": "option",
                        "label": "Option",
                        "name": "option",
                    },
                    {
                        "id": "q5",
                        "type": "multiple_option",
                        "label": "Multiple",
                        "name": "multiple",
                    },
                    {
                        "id": "q6",
                        "type": "image",
                        "label": "Photo",
                        "name": "photo",
                    },
                    {"id": "q7", "type": "geo", "label": "Geo", "name": "geo"},
                    {
                        "id": "q8",
                        "type": "cascade",
                        "label": "Cascade",
                        "name": "cascade",
                    },
                    {
                        "id": "q9",
                        "type": "table",
                        "label": "Table",
                        "name": "table",
                    },
                    {
                        "id": "q10",
                        "type": "tree",
                        "label": "Tree",
                        "name": "tree",
                    },
                    {
                        "id": "q11",
                        "type": "signature",
                        "label": "Signature",
                        "name": "signature",
                    },
                ],
            }
        ],
    }

    parser = AkvoReactFormParser()
    result = parser.parse(form_json)

    type_mapping = {
        "input": QuestionType.INPUT,
        "number": QuestionType.NUMBER,
        "date": QuestionType.DATE,
        "option": QuestionType.OPTION,
        "multiple_option": QuestionType.MULTIPLE_OPTION,
        "image": QuestionType.IMAGE,
        "geo": QuestionType.GEO,
        "cascade": QuestionType.CASCADE,
        "table": QuestionType.TABLE,
        "tree": QuestionType.TREE,
        "signature": QuestionType.SIGNATURE,
    }

    for i, (type_str, enum_type) in enumerate(type_mapping.items(), 1):
        question = result.sections[0].questions[i - 1]
        assert question.type == enum_type, f"Failed for type {type_str}"


def test_parser_handles_empty_form():
    form_json = {"name": "Empty Form", "question_group": []}
    parser = AkvoReactFormParser()
    result = parser.parse(form_json)
    assert len(result.sections) == 0


def test_parser_handles_empty_questions():
    form_json = {
        "name": "Empty Questions",
        "question_group": [{"name": "Empty Group", "order": 1, "question": []}],
    }
    parser = AkvoReactFormParser()
    result = parser.parse(form_json)
    assert len(result.sections) == 1
    assert len(result.sections[0].questions) == 0


def test_parser_handles_missing_optional_fields():
    form_json = {
        "name": "Minimal Form",
        "question_group": [
            {
                "name": "Minimal Group",
                "order": 1,
                "question": [
                    {
                        "id": "q1",
                        "name": "basic",
                        "type": "input",
                        "label": "Basic Question",
                    }
                ],
            }
        ],
    }
    parser = AkvoReactFormParser()
    result = parser.parse(form_json)
    q = result.sections[0].questions[0]
    assert q.answer.required is False
    assert q.answer.options == []
    assert q.answer.allowOther is False
    assert q.answer.minValue is None
    assert q.answer.maxValue is None
    assert q.dependencies == []


def test_parser_handles_complex_dependencies():
    form_json = {
        "name": "Dependencies Form",
        "question_group": [
            {
                "name": "Dependencies",
                "order": 1,
                "question": [
                    {
                        "id": "q1",
                        "name": "trigger",
                        "type": "option",
                        "label": "Trigger Question",
                        "option": [
                            {"label": "Yes", "value": "yes"},
                            {"label": "No", "value": "no"},
                        ],
                    },
                    {
                        "id": "q2",
                        "name": "dependent",
                        "type": "input",
                        "label": "Dependent Question",
                        "dependency": [{"id": "q1", "options": ["yes"]}],
                    },
                ],
            }
        ],
    }
    parser = AkvoReactFormParser()
    result = parser.parse(form_json)
    q2 = result.sections[0].questions[1]
    assert len(q2.dependencies) == 1
    assert q2.dependencies[0].depends_on_question_id == "q1"
    assert q2.dependencies[0].expected_answer == "yes"
