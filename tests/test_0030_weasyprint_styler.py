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

    form = styler.inject_question_numbers(form)

    # Section letter assignment
    assert form.sections[0].letter is None
    assert form.sections[1].letter is None

    # Question number assignment
    assert form.sections[0].questions[0].number == 1
    assert form.sections[1].questions[0].number == 2


def test_render_html_and_pdf_with_flow_parser():
    styler = WeasyPrintStyler()
    parser_type = "flow"
    # Contoh data JSON minimal AkvoFlow
    flow_json = {
        "name": "Sample Flow Form",
        "questionGroup": [
            {
                "heading": "Section 1",
                "question": {
                    "id": "q1",
                    "type": "free",
                    "text": "What is your name?",
                },
            },
            {
                "heading": "Section 2",
                "question": {
                    "id": "q2",
                    "type": "option",
                    "text": "Select one",
                    "options": {"option": [{"text": "A"}, {"text": "B"}]},
                },
            },
        ],
    }

    html_content = styler.render_html(flow_json, parser_type)
    assert "<html" in html_content.lower()
    assert "Sample Flow Form" in html_content

    pdf_content = styler.render_pdf(flow_json, parser_type)
    assert isinstance(pdf_content, bytes)
    assert len(pdf_content) > 1000  # arbitrary minimal size check


def test_render_html_and_pdf_with_arf_parser():
    styler = WeasyPrintStyler()
    parser_type = "arf"
    # Contoh data JSON minimal ARF (disesuaikan dengan parser ARF Anda)
    arf_json = {
        "name": "Sample ARF Form",
        "question_group": [
            {
                "name": "Section A",
                "question": [
                    {"id": 1, "name": "ARF Question 1", "type": "input"},
                    {
                        "id": 2,
                        "name": "ARF Question 2",
                        "type": "option",
                        "option": [{"label": "Male"}, {"label": "Female"}],
                    },
                ],
            }
        ],
    }

    html_content = styler.render_html(arf_json, parser_type)
    assert "<html" in html_content.lower()
    assert "Sample ARF Form" in html_content

    pdf_content = styler.render_pdf(arf_json, parser_type)
    assert isinstance(pdf_content, bytes)
    assert len(pdf_content) > 1000  # arbitrary minimal size check
