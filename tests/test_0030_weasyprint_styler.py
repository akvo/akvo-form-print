from AkvoFormPrint.stylers.weasyprint_styler import WeasyPrintStyler
from AkvoFormPrint.models import (
    FormModel,
    FormSection,
    QuestionItem,
    AnswerField,
)
from AkvoFormPrint.enums import QuestionType


def test_number_to_letter_mapping():
    styler = WeasyPrintStyler()

    assert styler._number_to_letter(0) == "A"
    assert styler._number_to_letter(1) == "B"
    assert styler._number_to_letter(25) == "Z"
    assert styler._number_to_letter(26) == "AA"
    assert styler._number_to_letter(27) == "AB"
    assert styler._number_to_letter(51) == "AZ"
    assert styler._number_to_letter(52) == "BA"


def test_inject_question_numbers_and_section_letters():
    styler = WeasyPrintStyler()

    # Create mock form with 2 sections, each has 1 question
    form = FormModel(
        title="Sample Form",
        sections=[
            FormSection(
                title="Section One",
                questions=[
                    QuestionItem(
                        id="q1",
                        label="First question",
                        type=QuestionType.INPUT,
                        answer=AnswerField(id="q1", type=QuestionType.INPUT),
                    )
                ],
            ),
            FormSection(
                title="Section Two",
                questions=[
                    QuestionItem(
                        id="q2",
                        label="Second question",
                        type=QuestionType.OPTION,
                        answer=AnswerField(id="q2", type=QuestionType.OPTION),
                    )
                ],
            ),
        ],
    )

    styler.inject_question_numbers(form)

    # Section letter assignment
    assert form.sections[0].letter == "A"
    assert form.sections[1].letter == "B"

    # Question number assignment
    assert form.sections[0].questions[0].number == 1
    assert form.sections[1].questions[0].number == 2
