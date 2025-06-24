import pytest
from AkvoFormPrint.parsers.akvo_flow_parser import AkvoFlowFormParser
from AkvoFormPrint.enums import QuestionType
from AkvoFormPrint.models import FormModel
from AkvoFormPrint.constant import TEXT_ROWS


@pytest.fixture
def raw_form_json():
    return {
        "name": "Sample Form",
        "questionGroup": [
            {
                "heading": "Section 1",
                "repeatable": True,
                "question": [
                    {
                        "id": "q1",
                        "text": "What is your name?",
                        "type": "free",
                        "mandatory": True,
                        "variableName": "",
                    },
                    {
                        "id": "q2",
                        "text": "Choose your favorite fruit",
                        "type": "option",
                        "mandatory": False,
                        "options": {
                            "option": [
                                {"text": "Apple"},
                                {"text": "Banana"},
                            ],
                            "allowOther": True,
                            "allowMultiple": False,
                        },
                    },
                    {
                        "id": "q3",
                        "text": "Pick all that apply",
                        "type": "option",
                        "options": {
                            "option": [
                                {"text": "Option A"},
                                {"text": "Option B"},
                            ],
                            "allowMultiple": True,
                        },
                    },
                    {
                        "id": "q4",
                        "text": "Enter your age",
                        "type": "free",
                        "validationRule": {
                            "validationType": "numeric",
                            "maxVal": "120",
                        },
                    },
                    {"id": "q5", "text": "Location?", "type": "geo"},
                    {
                        "id": "q6",
                        "text": "Why did you choose other?",
                        "type": "free",
                        "help": {
                            "text": "Example tooltip",
                        },
                        "dependency": {
                            "question": "q2",
                            "answer-value": "Other",
                        },
                    },
                    {
                        "id": "q7",
                        "text": "Cascading option",
                        "type": "cascade",
                        "levels": {
                            "level": [{"text": "Level 1"}, {"text": "Level 2"}]
                        },
                    },
                    {
                        "id": "q8",
                        "text": "Comment textbox",
                        "type": "free",
                        "mandatory": False,
                        "variableName": "textbox_1",
                    },
                    {
                        "id": "q9",
                        "text": "Comment textbox with 5 rows",
                        "type": "free",
                        "mandatory": False,
                        "variableName": "textbox_2_5",
                    },
                    {
                        "id": "q10",
                        "text": "Example instruction",
                        "type": "free",
                        "mandatory": False,
                        "variableName": "INSTRUCTION_1",
                    },
                ],
            }
        ],
    }


def test_parser_generates_correct_form_model(raw_form_json):
    parser = AkvoFlowFormParser()
    result: FormModel = parser.parse(raw_form_json)

    assert result.title == "Sample Form"
    assert len(result.sections) == 1

    section = result.sections[0]
    assert section.title == "Section 1"
    assert len(section.questions) == 10

    q1 = section.questions[0]
    assert q1.id == "q1"
    assert q1.type == QuestionType.INPUT
    assert q1.answer.required is True
    assert q1.answer.textRows is None

    q2 = section.questions[1]
    assert q2.type == QuestionType.OPTION
    assert q2.answer.allowOther is True
    assert q2.answer.options == ["Apple", "Banana"]

    q3 = section.questions[2]
    assert q3.type == QuestionType.MULTIPLE_OPTION

    q4 = section.questions[3]
    assert q4.type == QuestionType.NUMBER
    assert q4.answer.numberBox == 3

    q5 = section.questions[4]
    assert q5.type == QuestionType.GEO

    q6 = section.questions[5]
    assert len(q6.dependencies) == 1
    assert q6.dependencies[0].depends_on_question_id == "q2"
    assert q6.dependencies[0].expected_answer == "Other"

    q7 = section.questions[6]
    assert q7.type == QuestionType.CASCADE
    assert q7.answer.options == ["Level 1", "Level 2"]

    q8 = section.questions[7]
    assert q8.type == QuestionType.TEXT
    assert q8.answer.textRows == TEXT_ROWS

    q9 = section.questions[8]
    assert q9.type == QuestionType.TEXT
    assert q9.answer.textRows == 5

    q10 = section.questions[9]
    assert q10.type == QuestionType.INSTRUCTION
