import pytest
from AkvoFormPrint.parsers.default_parser import DefaultParser
from AkvoFormPrint.enums import QuestionType
from AkvoFormPrint.models import FormModel


@pytest.fixture
def raw_form_json():
    return {
        "title": "Sample Default Form",
        "sections": [
            {
                "title": "Basic Information",
                "questions": [
                    {
                        "id": "q1",
                        "type": "input",
                        "label": "What is your name?",
                        "required": True,
                    },
                    {
                        "id": "q2",
                        "type": "number",
                        "label": "Age",
                        "required": True,
                        "minValue": 0,
                        "maxValue": 120,
                    },
                    {
                        "id": "q3",
                        "type": "option",
                        "label": "Gender",
                        "options": ["Male", "Female", "Other"],
                        "allowOther": True,
                        "optionSingleLine": True,
                    },
                    {
                        "id": "q4",
                        "type": "multiple_option",
                        "label": "Select all that apply",
                        "options": ["A", "B", "C"],
                    },
                    {
                        "id": "q5",
                        "type": "text",
                        "label": "Additional comments",
                        "dependencies": [
                            {
                                "depends_on_question_id": "q3",
                                "expected_answer": "Other",
                            }
                        ],
                    },
                ],
            }
        ],
    }


def test_parser_generates_correct_form_model(raw_form_json):
    parser = DefaultParser()
    result: FormModel = parser.parse(raw_form_json)

    assert result.title == "Sample Default Form"
    assert len(result.sections) == 1

    section = result.sections[0]
    assert section.title == "Basic Information"
    assert len(section.questions) == 5

    # Test input question
    q1 = section.questions[0]
    assert q1.id == "q1"
    assert q1.type == QuestionType.INPUT
    assert q1.label == "What is your name?"
    assert q1.answer.required is True

    # Test number question with min/max
    q2 = section.questions[1]
    assert q2.type == QuestionType.NUMBER
    assert q2.answer.minValue == 0
    assert q2.answer.maxValue == 120

    # Test option question with allowOther and optionSingleLine
    q3 = section.questions[2]
    assert q3.type == QuestionType.OPTION
    assert q3.answer.options == ["Male", "Female", "Other"]
    assert q3.answer.allowOther is True
    assert q3.answer.optionSingleLine is True

    # Test multiple option question
    q4 = section.questions[3]
    assert q4.type == QuestionType.MULTIPLE_OPTION
    assert q4.answer.options == ["A", "B", "C"]
    assert q4.answer.allowOther is False

    # Test dependencies
    q5 = section.questions[4]
    assert q5.type == QuestionType.TEXT
    assert len(q5.dependencies) == 1
    assert q5.dependencies[0].depends_on_question_id == "q3"
    assert q5.dependencies[0].expected_answer == "Other"


def test_parser_handles_all_question_types():
    form_json = {
        "title": "All Types Form",
        "sections": [
            {
                "title": "All Types",
                "questions": [
                    {"id": "q1", "type": "input", "label": "Input"},
                    {"id": "q2", "type": "number", "label": "Number"},
                    {"id": "q3", "type": "text", "label": "Text"},
                    {"id": "q4", "type": "date", "label": "Date"},
                    {"id": "q5", "type": "option", "label": "Option"},
                    {
                        "id": "q6",
                        "type": "multiple_option",
                        "label": "Multiple",
                    },
                    {"id": "q7", "type": "image", "label": "Image"},
                    {"id": "q8", "type": "geo", "label": "Geo"},
                    {"id": "q9", "type": "cascade", "label": "Cascade"},
                    {"id": "q10", "type": "table", "label": "Table"},
                    {"id": "q11", "type": "autofield", "label": "Auto"},
                    {"id": "q12", "type": "tree", "label": "Tree"},
                    {"id": "q13", "type": "signature", "label": "Signature"},
                ],
            }
        ],
    }

    parser = DefaultParser()
    result = parser.parse(form_json)

    type_mapping = {
        "input": QuestionType.INPUT,
        "number": QuestionType.NUMBER,
        "text": QuestionType.TEXT,
        "date": QuestionType.DATE,
        "option": QuestionType.OPTION,
        "multiple_option": QuestionType.MULTIPLE_OPTION,
        "image": QuestionType.IMAGE,
        "geo": QuestionType.GEO,
        "cascade": QuestionType.CASCADE,
        "table": QuestionType.TABLE,
        "autofield": QuestionType.AUTOFIELD,
        "tree": QuestionType.TREE,
        "signature": QuestionType.SIGNATURE,
    }

    for i, (type_str, enum_type) in enumerate(type_mapping.items(), 1):
        question = result.sections[0].questions[i - 1]
        assert question.type == enum_type, f"Failed for type {type_str}"


def test_parser_handles_empty_sections():
    form_json = {"title": "Empty Form", "sections": []}
    parser = DefaultParser()
    result = parser.parse(form_json)
    assert len(result.sections) == 0


def test_parser_handles_empty_questions():
    form_json = {
        "title": "Empty Questions",
        "sections": [{"title": "Empty Section", "questions": []}],
    }
    parser = DefaultParser()
    result = parser.parse(form_json)
    assert len(result.sections) == 1
    assert len(result.sections[0].questions) == 0


def test_parser_handles_missing_optional_fields():
    form_json = {
        "title": "Minimal Form",
        "sections": [
            {
                "title": "Minimal Section",
                "questions": [{"id": "q1", "type": "input", "label": "Basic"}],
            }
        ],
    }
    parser = DefaultParser()
    result = parser.parse(form_json)
    q = result.sections[0].questions[0]
    assert q.answer.required is False
    assert q.answer.options == []
    assert q.answer.allowOther is False
    assert q.answer.optionSingleLine is False
    assert q.answer.minValue is None
    assert q.answer.maxValue is None
    assert q.dependencies is None
