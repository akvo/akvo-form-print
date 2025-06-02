from AkvoFormPrint.models import (
    QuestionDependency,
    AnswerField,
    QuestionItem,
    FormSection,
    FormModel,
)
from AkvoFormPrint.enums import QuestionType, HintText


def test_question_dependency_model():
    dep = QuestionDependency(depends_on_question_id="q1", expected_answer="Yes")
    assert dep.depends_on_question_id == "q1"
    assert dep.expected_answer == "Yes"


def test_answer_field_defaults():
    answer = AnswerField(
        id="q1",
        type=QuestionType.INPUT,
        required=True,
    )
    assert answer.id == "q1"
    assert answer.type == QuestionType.INPUT
    assert answer.required is True
    assert answer.options == []
    assert answer.repeat is False
    assert answer.allowOther is False
    assert answer.numberBox == 10
    assert answer.optionSingleLine is False


def test_question_item_hint_mapping_option():
    item = QuestionItem(
        id="q1",
        label="What is your favorite color?",
        type=QuestionType.OPTION,
        answer=AnswerField(id="q1", type=QuestionType.OPTION, required=False),
    )
    assert item.hint == HintText.OPTION


def test_question_item_hint_mapping_multiple_option():
    item = QuestionItem(
        id="q2",
        label="Select your hobbies",
        type=QuestionType.MULTIPLE_OPTION,
        answer=AnswerField(id="q2", type=QuestionType.MULTIPLE_OPTION),
    )
    assert item.hint == HintText.MULTIPLE_OPTION


def test_question_item_hint_mapping_other_type():
    item = QuestionItem(
        id="q3",
        label="Enter your name",
        type=QuestionType.INPUT,
        answer=AnswerField(id="q3", type=QuestionType.INPUT),
    )
    assert item.hint is None


def test_form_section_model():
    item = QuestionItem(
        id="q1",
        label="Test",
        type=QuestionType.INPUT,
        answer=AnswerField(id="q1", type=QuestionType.INPUT),
    )
    section = FormSection(title="Section A", questions=[item])
    assert section.title == "Section A"
    assert len(section.questions) == 1
    assert section.questions[0].id == "q1"


def test_form_model_question_id_to_info():
    item = QuestionItem(
        id="q1",
        label="Test",
        type=QuestionType.INPUT,
        number=1,
        answer=AnswerField(id="q1", type=QuestionType.INPUT),
    )
    section = FormSection(title="Section A", questions=[item])
    section.letter = "A"

    form = FormModel(
        title="Form X",
        sections=[section],
    )
    info = form.question_id_to_info
    assert info["q1"] == ("A.1", "Test")


def test_form_model_reverse_dependency_map():
    dependent = QuestionItem(
        id="q2",
        label="Why?",
        type=QuestionType.INPUT,
        dependencies=[
            QuestionDependency(depends_on_question_id="q1", expected_answer="Yes")
        ],
        answer=AnswerField(id="q2", type=QuestionType.INPUT),
        number=2,
    )
    section = FormSection(title="Section A", questions=[dependent])
    section.letter = "A"  # Inject section letter manually for test

    form = FormModel(title="Form", sections=[section])
    reverse_map = form.question_reverse_dependency_map

    assert "q1" in reverse_map

    # Get the list of (code, question) tuples
    reverse_entries = reverse_map["q1"]
    assert isinstance(reverse_entries[0], tuple)
    assert reverse_entries[0][0] == "A.2"
    assert reverse_entries[0][1].id == "q2"
