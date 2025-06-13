import os

from AkvoFormPrint.stylers.docx_renderer import DocxRenderer, Document
from AkvoFormPrint.models import (
    FormModel,
    FormSection,
    QuestionItem,
    QuestionType,
    AnswerField,
)


def extract_all_table_texts(doc):
    return [
        [cell.text for cell in row.cells]
        for table in doc.tables
        for row in table.rows
    ]


def test_number_to_letter_mapping():
    styler = DocxRenderer()

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

    # Test with question numbering disabled
    styler = DocxRenderer(
        add_section_numbering=False, add_question_numbering=False
    )
    form = styler._inject_question_numbers(form)

    # Section letter assignment
    assert form.sections[0].letter is None
    assert form.sections[1].letter is None

    # Question numbers should be None when disabled
    assert form.sections[0].questions[0].number is None
    assert form.sections[1].questions[0].number is None

    # Test with question numbering enabled
    styler = DocxRenderer(
        add_section_numbering=False, add_question_numbering=True
    )
    form = styler._inject_question_numbers(form)

    # Question numbers should be sequential when enabled
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

    # Test with both section letters and question numbers
    styler = DocxRenderer(
        add_section_numbering=True, add_question_numbering=True
    )
    form = styler._inject_question_numbers(form)

    # Section letter assignment
    assert form.sections[0].letter == "A"
    assert form.sections[1].letter == "B"

    # Question number assignment
    assert form.sections[0].questions[0].number == 1
    assert form.sections[1].questions[0].number == 2

    # Test with section letters but no question numbers
    styler = DocxRenderer(
        add_section_numbering=True, add_question_numbering=False
    )
    form = styler._inject_question_numbers(form)

    # Section letters should still be assigned
    assert form.sections[0].letter == "A"
    assert form.sections[1].letter == "B"

    # Question numbers should be None
    assert form.sections[0].questions[0].number is None
    assert form.sections[1].questions[0].number is None


def test_docx_renderer_with_with_flow_json_format(tmp_path):
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

    output_path = tmp_path / "sample_output.docx"

    renderer = DocxRenderer(
        orientation="portrait",
        add_section_numbering=True,
        add_question_numbering=True,
        parser_type="flow",
        raw_json=flow_json,
        output_path=str(output_path),
    )

    renderer.render_docx()

    assert os.path.exists(output_path)

    # Optionally check contents
    doc = Document(str(output_path))
    doc_text = "\n".join([p.text for p in doc.paragraphs])
    table_texts = extract_all_table_texts(doc)

    assert "Sample Flow Form" in doc_text
    assert "Section 1" in doc_text
    assert "What is your name?" in doc_text
    assert "Select one" in doc_text
    assert any("( ) A" in cell for row in table_texts for cell in row)
    assert any("( ) B" in cell for row in table_texts for cell in row)


def test_docx_renderer_with_with_arf_json_format(tmp_path):
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

    output_path = tmp_path / "sample_output.docx"

    renderer = DocxRenderer(
        orientation="landscape",
        add_section_numbering=True,
        add_question_numbering=True,
        parser_type="arf",
        raw_json=arf_json,
        output_path=str(output_path),
    )

    renderer.render_docx()

    assert os.path.exists(output_path)

    # Optionally check contents
    doc = Document(str(output_path))
    doc_text = "\n".join([p.text for p in doc.paragraphs])
    table_texts = extract_all_table_texts(doc)

    assert "Sample ARF Form" in doc_text
    assert "Section A" in doc_text
    assert "ARF Question 1" in doc_text
    assert "ARF Question 2" in doc_text
    assert any("( ) Male" in cell for row in table_texts for cell in row)
    assert any("( ) Female" in cell for row in table_texts for cell in row)


def test_docx_renderer_with_default_json_format(tmp_path):
    default_json = {
        "title": "Sample Form",
        "sections": [
            {
                "title": "Section A",
                "questions": [
                    {
                        "id": "q1",
                        "label": "What is your name?",
                        "type": "text",
                        "required": True,
                    },
                    {
                        "id": "q2",
                        "label": "Your favorite fruit?",
                        "type": "multiple_option",
                        "required": False,
                        "options": ["Apple", "Banana"],
                        "allowOther": True,
                    },
                ],
            }
        ],
    }

    output_path = tmp_path / "sample_output.docx"

    renderer = DocxRenderer(
        orientation="portrait",
        add_section_numbering=True,
        add_question_numbering=True,
        parser_type="default",
        raw_json=default_json,
        output_path=str(output_path),
    )

    renderer.render_docx()

    assert os.path.exists(output_path)

    # Optionally check contents
    doc = Document(str(output_path))
    doc_text = "\n".join([p.text for p in doc.paragraphs])
    table_texts = extract_all_table_texts(doc)

    assert "Sample Form" in doc_text
    assert "Section A" in doc_text
    assert "What is your name?" in doc_text
    assert "Your favorite fruit?" in doc_text
    assert any("[ ] Apple" in cell for row in table_texts for cell in row)
    assert any("[ ] Banana" in cell for row in table_texts for cell in row)
