from AkvoFormPrint.stylers.weasyprint_styler import WeasyPrintStyler
from AkvoFormPrint.models import (
    FormModel,
    FormSection,
    QuestionItem,
    AnswerField,
)
from AkvoFormPrint.enums import QuestionType
import pytest
import os


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


@pytest.fixture
def sample_form_json():
    return {
        "title": "Test Form",
        "sections": [
            {
                "title": "Section 1",
                "questions": [
                    {
                        "id": "q1",
                        "type": "input",
                        "label": "Question 1",
                        "required": True,
                    },
                    {
                        "id": "q2",
                        "type": "option",
                        "label": "Question 2",
                        "options": ["A", "B", "C"],
                        "allowOther": True,
                    },
                ],
            },
            {
                "title": "Section 2",
                "questions": [
                    {
                        "id": "q3",
                        "type": "multiple_option",
                        "label": "Question 3",
                        "options": ["X", "Y", "Z"],
                    }
                ],
            },
        ],
    }


def test_styler_initialization(sample_form_json):
    styler = WeasyPrintStyler(
        orientation="landscape",
        add_section_numbering=True,
        parser_type="default",
        raw_json=sample_form_json,
    )

    assert styler.orientation == "landscape"
    assert styler.add_section_numbering is True
    assert isinstance(styler.form_model, FormModel)
    assert styler.form_model.title == "Test Form"
    assert len(styler.form_model.sections) == 2


def test_styler_with_different_orientations(sample_form_json):
    # Test landscape
    landscape_styler = WeasyPrintStyler(
        orientation="landscape", raw_json=sample_form_json
    )
    landscape_html = landscape_styler.render_html()
    assert "landscape" in landscape_html.lower()

    # Test portrait
    portrait_styler = WeasyPrintStyler(
        orientation="portrait", raw_json=sample_form_json
    )
    portrait_html = portrait_styler.render_html()
    assert "portrait" in portrait_html.lower()


def test_styler_section_numbering(sample_form_json):
    # With section numbering
    numbered_styler = WeasyPrintStyler(
        add_section_numbering=True, raw_json=sample_form_json
    )
    numbered_html = numbered_styler.render_html()
    print(numbered_html)
    assert "A. Section 1" in numbered_html
    assert "B. Section 2" in numbered_html

    # Without section numbering
    plain_styler = WeasyPrintStyler(
        add_section_numbering=False, raw_json=sample_form_json
    )
    plain_html = plain_styler.render_html()
    assert "Section 1" in plain_html
    assert "Section 2" in plain_html


def test_styler_question_rendering(sample_form_json):
    styler = WeasyPrintStyler(raw_json=sample_form_json)
    html = styler.render_html()

    # Check required field marking
    assert "*" in html  # Required field marker

    # Check option rendering
    assert "A" in html
    assert "B" in html
    assert "C" in html
    assert "Other" in html  # allowOther option

    # Check multiple option rendering
    assert "X" in html
    assert "Y" in html
    assert "Z" in html


def test_styler_pdf_generation(sample_form_json, tmp_path):
    output_path = os.path.join(tmp_path, "test.pdf")

    styler = WeasyPrintStyler(raw_json=sample_form_json)
    pdf_content = styler.render_pdf()

    # Write PDF to temp file
    with open(output_path, "wb") as f:
        f.write(pdf_content)

    # Check if PDF was created and has content
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0


def test_styler_with_different_parsers():
    # Test with Flow parser
    flow_json = {
        "name": "Flow Form",
        "questionGroup": [
            {
                "heading": "Flow Section",
                "question": [{"id": "q1", "text": "Flow Question", "type": "free"}],
            }
        ],
    }

    flow_styler = WeasyPrintStyler(parser_type="flow", raw_json=flow_json)
    flow_html = flow_styler.render_html()
    assert "Flow Section" in flow_html
    assert "Flow Question" in flow_html

    # Test with ARF parser
    arf_json = {
        "name": "ARF Form",
        "question_group": [
            {
                "name": "ARF Section",
                "question": [
                    {
                        "id": "q1",
                        "name": "arf_q",
                        "type": "text",
                        "label": "ARF Question",
                    }
                ],
            }
        ],
    }

    arf_styler = WeasyPrintStyler(parser_type="arf", raw_json=arf_json)
    arf_html = arf_styler.render_html()
    assert "ARF Section" in arf_html
    assert "ARF Question" in arf_html


def test_styler_handles_empty_form():
    empty_json = {"title": "Empty Form", "sections": []}

    styler = WeasyPrintStyler(raw_json=empty_json)
    html = styler.render_html()

    assert "Empty Form" in html
    assert len(styler.form_model.sections) == 0


def test_styler_handles_dependencies(sample_form_json):
    # Add dependency to the form
    sample_form_json["sections"][1]["questions"][0]["dependencies"] = [
        {"depends_on_question_id": "q2", "expected_answer": "A"}
    ]

    styler = WeasyPrintStyler(raw_json=sample_form_json)
    html = styler.render_html()

    # Check if dependency info is in the HTML
    print(html)
    assert 'If "A": go to question 3'
    assert '"A" selected for question 2: "Question 2"' in html


def test_styler_error_handling():
    # Test invalid orientation
    with pytest.raises(
        AssertionError, match="Orientation must be 'portrait' or 'landscape'"
    ):
        WeasyPrintStyler(
            orientation="invalid", raw_json={"title": "Test", "sections": []}
        )

    # Test invalid parser type
    with pytest.raises(ValueError, match="Unknown parser type: invalid"):
        WeasyPrintStyler(
            parser_type="invalid", raw_json={"title": "Test", "sections": []}
        )

    # Test missing raw_json when trying to parse
    styler = WeasyPrintStyler()
    with pytest.raises(ValueError, match="No raw_json data provided to parse"):
        styler.render_html()
