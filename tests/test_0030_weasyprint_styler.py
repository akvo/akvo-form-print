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


def test_inject_question_numbers_without_section_letters():
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

    styler = WeasyPrintStyler(add_section_numbering=False)
    form = styler.inject_question_numbers(form)

    # Section letter assignment
    assert form.sections[0].letter is None
    assert form.sections[1].letter is None

    # Question number assignment
    assert form.sections[0].questions[0].number == 1
    assert form.sections[1].questions[0].number == 2


def test_inject_question_numbers_with_section_letters():
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

    styler = WeasyPrintStyler(add_section_numbering=True)
    form = styler.inject_question_numbers(form)

    # Section letter assignment
    assert form.sections[0].letter == "A"
    assert form.sections[1].letter == "B"

    # Question number assignment
    assert form.sections[0].questions[0].number == 1
    assert form.sections[1].questions[0].number == 2


def test_render_html_and_pdf_with_flow_parser():
    # Sample Flow form data
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

    styler = WeasyPrintStyler(
        parser_type="flow",
        raw_json=flow_json,
        orientation="landscape",
        add_section_numbering=True,
    )

    # Test HTML rendering
    html_content = styler.render_html()
    assert "<html" in html_content.lower()
    assert "Sample Flow Form" in html_content
    assert 'class="landscape"' in html_content

    # Test PDF rendering
    pdf_content = styler.render_pdf()
    assert isinstance(pdf_content, bytes)
    assert len(pdf_content) > 1000  # arbitrary minimal size check


def test_render_html_and_pdf_with_arf_parser():
    # Sample ARF form data
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

    styler = WeasyPrintStyler(
        parser_type="arf",
        raw_json=arf_json,
        orientation="portrait",
        add_section_numbering=False,
    )

    # Test HTML rendering
    html_content = styler.render_html()
    assert "<html" in html_content.lower()
    assert "Sample ARF Form" in html_content
    assert 'class="portrait"' in html_content

    # Test PDF rendering
    pdf_content = styler.render_pdf()
    assert isinstance(pdf_content, bytes)
    assert len(pdf_content) > 1000  # arbitrary minimal size check


def test_render_html_and_pdf_with_default_parser():
    # Sample default form data
    default_json = {
        "title": "Sample Default Form",
        "sections": [
            {
                "title": "Section 1",
                "questions": [
                    {
                        "id": "q1",
                        "type": "input",
                        "label": "What is your name?",
                    }
                ],
            }
        ],
    }

    styler = WeasyPrintStyler(
        raw_json=default_json,  # parser_type defaults to "default"
        orientation="landscape",
    )

    # Test HTML rendering
    html_content = styler.render_html()
    assert "<html" in html_content.lower()
    assert "Sample Default Form" in html_content
    assert 'class="landscape"' in html_content

    # Test PDF rendering
    pdf_content = styler.render_pdf()
    assert isinstance(pdf_content, bytes)
    assert len(pdf_content) > 1000  # arbitrary minimal size check
