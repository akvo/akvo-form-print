from typing import Any, Dict, Optional
from docx import Document
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

from AkvoFormPrint.parsers.akvo_flow_parser import AkvoFlowFormParser
from AkvoFormPrint.parsers.akvo_arf_parser import AkvoReactFormParser
from AkvoFormPrint.parsers.default_parser import DefaultParser
from AkvoFormPrint.parsers.base_parser import BaseParser


class DocxRenderer:
    def __init__(
        self,
        orientation: str = "landscape",
        add_section_numbering: bool = False,
        add_question_numbering: bool = True,
        parser_type: Optional[str] = None,
        raw_json: Optional[Dict[str, Any]] = None,
        output_path: Optional[str] = "output.docx",
    ):
        """Initialize DocxRenderer with configuration."""
        assert orientation in (
            "portrait",
            "landscape",
        ), "Orientation must be 'portrait' or 'landscape'"
        self.orientation = orientation
        self.add_section_numbering = add_section_numbering
        self.add_question_numbering = add_question_numbering
        self.parser_type = parser_type
        self.raw_json = raw_json
        self.output_path = output_path

        self.parser: Optional[BaseParser] = None
        self.form_model = None
        self.doc = Document()

        if parser_type or raw_json:
            self.parser = self._get_parser(parser_type)

        if self.raw_json:
            self.form_model = self._parse_form()

    def _get_parser(self, parser_type: Optional[str] = None) -> BaseParser:
        if parser_type == "flow":
            return AkvoFlowFormParser()
        elif parser_type == "arf":
            return AkvoReactFormParser()
        elif parser_type is None or parser_type == "default":
            return DefaultParser()
        else:
            raise ValueError(f"Unknown parser type: {parser_type}")

    def _parse_form(self):
        if not self.raw_json:
            raise ValueError("No raw_json data provided to parse")
        if not self.parser:
            self.parser = self._get_parser(self.parser_type)
        form_model = self.parser.parse(self.raw_json)
        return self._inject_question_numbers(form_model)

    def _inject_question_numbers(self, form):
        section_index = 0
        counter = 1
        for section in form.sections:
            section.letter = (
                self._number_to_letter(section_index)
                if self.add_section_numbering
                else None
            )
            if self.add_section_numbering:
                section_index += 1
            for question in section.questions:
                question.number = (
                    counter if self.add_question_numbering else None
                )
                if self.add_question_numbering:
                    counter += 1
        return form

    def _number_to_letter(self, n: int) -> str:
        """Convert a zero-based index to letters (A, B, ..., Z, AA, AB, ...)."""
        result = ""
        while n >= 0:
            result = chr(n % 26 + ord("A")) + result
            n = n // 26 - 1
        return result

    def _set_landscape(self):
        """Set the document orientation to landscape with specific margins."""
        section = self.doc.sections[-1]
        section.orientation = WD_ORIENT.LANDSCAPE
        section.page_width, section.page_height = (
            section.page_height,
            section.page_width,
        )
        for side in [
            "top_margin",
            "bottom_margin",
            "left_margin",
            "right_margin",
        ]:
            setattr(section, side, Inches(0.5))

    def render_docx(self):
        """Render the DOCX document with the parsed form model."""
        if not self.form_model:
            self.form_model = self._parse_form()

        if self.orientation == "landscape":
            self._set_landscape()

        # Title
        self.doc.add_paragraph(self.form_model.title, style="Title")

        # Enable 2-column layout
        section = self.doc.sections[-1]
        sectPr = section._sectPr
        cols_elem = sectPr.xpath("./w:cols")
        cols = cols_elem[0] if cols_elem else OxmlElement("w:cols")
        cols.set(qn("w:num"), "2")
        if not cols_elem:
            sectPr.append(cols)

        # Sections and questions
        for idx, section_data in enumerate(self.form_model.sections):
            if idx != 0:
                self.doc.add_page_break()

            # Section title
            section_title = (
                f"{section_data.letter}. {section_data.title}"
                if section_data.letter
                else section_data.title
            )
            self.doc.add_paragraph(section_title, style="Heading 1")

            # Questions
            for qidx, question in enumerate(section_data.questions):
                qtext = (
                    f"{question.number}. {question.label}"
                    if question.number
                    else question.label
                )
                para = self.doc.add_paragraph(qtext)
                para.style.font.size = Pt(11)

                if question.type.name in ["OPTION", "MULTIPLE_OPTION"]:
                    # Create a table directly in the document
                    table = self.doc.add_table(rows=1, cols=2)
                    table.autofit = True

                    # Remove empty paragraphs
                    for cell in [table.cell(0, 0), table.cell(0, 1)]:
                        p = cell.paragraphs[0]
                        p._element.getparent().remove(p._element)

                    # Fill columns with options
                    col1Len = 9 if qidx == 0 else 5
                    col1 = question.answer.options[:col1Len]
                    col2 = question.answer.options[col1Len:]

                    for opt in col1:
                        para = table.cell(0, 0).add_paragraph(f"☐ {opt}")
                        para.style.font.size = Pt(10)
                        para.paragraph_format.space_after = Pt(0)
                        para.paragraph_format.space_before = Pt(0)

                    for opt in col2:
                        para = table.cell(0, 1).add_paragraph(f"☐ {opt}")
                        para.style.font.size = Pt(10)
                        para.paragraph_format.space_after = Pt(0)
                        para.paragraph_format.space_before = Pt(0)
                else:
                    self.doc.add_paragraph("__________________________")

        self.doc.save(self.output_path)
