from typing import Any, Dict, Optional

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
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

        self.parser = None
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
        return self.inject_question_numbers(form_model)

    def inject_question_numbers(self, form):
        section_index = 0
        counter = 1
        for section in form.sections:
            if self.add_section_numbering:
                section.letter = self._number_to_letter(section_index)
                section_index += 1
            else:
                section.letter = None
            for question in section.questions:
                if self.add_question_numbering:
                    question.number = counter
                    counter += 1
                else:
                    question.number = None
        return form

    def _number_to_letter(self, n: int) -> str:
        result = ""
        while n >= 0:
            result = chr(n % 26 + ord("A")) + result
            n = n // 26 - 1
        return result

    def _set_landscape(self):
        section = self.doc.sections[-1]
        section.orientation = WD_ORIENT.LANDSCAPE
        new_width, new_height = section.page_height, section.page_width
        section.page_width = new_width
        section.page_height = new_height

        # Example margin
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

    def render_docx(self):
        if not self.form_model:
            self.form_model = self._parse_form()

        if self.orientation == "landscape":
            self._set_landscape()

        self.doc.add_paragraph(self.form_model.title, style="Title")

        # Set 2-column layout for the first section
        section = self.doc.sections[-1]
        sectPr = section._sectPr
        cols_elem = sectPr.xpath("./w:cols")
        if not cols_elem:
            cols = OxmlElement("w:cols")
            sectPr.append(cols)
        else:
            cols = cols_elem[0]
        cols.set(qn("w:num"), "2")

        for idx, section_data in enumerate(self.form_model.sections):
            if idx != 0:
                self.doc.add_page_break()

            section_title = (
                f"{section_data.letter}. {section_data.title}"
                if section_data.letter
                else section_data.title
            )
            self.doc.add_paragraph(section_title, style="Heading 1")

            for question in section_data.questions:
                qtext = (
                    f"{question.number}. {question.label}"
                    if question.number
                    else question.label
                )
                para = self.doc.add_paragraph(qtext)
                para.style.font.size = Pt(11)

                if question.type.name in ["OPTION", "MULTIPLE_OPTION"]:
                    for opt in question.answer.options:
                        opt_para = self.doc.add_paragraph(f"☐ {opt}")
                        opt_para.style.font.size = Pt(11)
                else:
                    self.doc.add_paragraph("__________________________")

        self.doc.save(self.output_path)
