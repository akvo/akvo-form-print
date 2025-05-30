from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from typing import Any, Dict

from AkvoFormPrint.parsers.akvo_flow_parser import AkvoFlowFormParser
from AkvoFormPrint.parsers.akvo_arf_parser import AkvoReactFormParser
from AkvoFormPrint.parsers.base_parser import BaseParser


class WeasyPrintStyler:
    def __init__(
        self,
        orientation: str = "landscape",
        add_section_numbering: bool = False,
    ):
        assert orientation in (
            "portrait",
            "landscape",
        ), "Orientation must be 'portrait' or 'landscape'"
        self.orientation = orientation
        self.add_section_numbering = add_section_numbering

        # Setup Jinja environment
        templates_path = Path(__file__).parent.parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(templates_path)))

        # Load CSS content once
        css_path = Path(__file__).parent.parent / "styles" / "default.css"
        self.css_content = css_path.read_text(encoding="utf-8")

    def inject_question_numbers(self, form):
        section_index = 0
        counter = 1
        for section in form.sections:
            if self.add_section_numbering:
                section.letter = self._number_to_letter(section_index)
            else:
                section.letter = None
            section_index += 1
            for question in section.questions:
                question.number = counter
                counter += 1
        return form

    def _get_parser(self, parser_type: str) -> BaseParser:
        if parser_type == "flow":
            return AkvoFlowFormParser()
        elif parser_type == "arf":
            return AkvoReactFormParser()
        else:
            raise ValueError(f"Unknown parser type: {parser_type}")

    def render_html(
        self,
        raw_json: Dict[str, Any],
        parser_type: str,
    ) -> str:
        parser = self._get_parser(parser_type)
        form_model = parser.parse(raw_json)
        form_model = self.inject_question_numbers(form_model)
        template = self.env.get_template("form_template.html")
        return template.render(
            form=form_model,
            css_content=self.css_content + self._get_page_css(),
            orientation=self.orientation,
        )

    def render_pdf(
        self,
        raw_json: Dict[str, Any],
        parser_type: str,
    ) -> bytes:
        parser = self._get_parser(parser_type)
        form_model = parser.parse(raw_json)
        form_model = self.inject_question_numbers(form_model)
        html_content = self.render_html(raw_json, parser_type)
        html = HTML(string=html_content)
        css = CSS(string=self.css_content + self._get_page_css())
        return html.write_pdf(stylesheets=[css])

    def _get_page_css(self) -> str:
        if self.orientation == "landscape":
            return """
            @page {
                size: A4 landscape;
                margin: 15mm;
            }
            """
        else:
            return """
            @page {
                size: A4 portrait;
                margin: 15mm;
            }
            """

    def _number_to_letter(self, n: int) -> str:
        """Convert number 0 -> A, 1 -> B, ..., 26 -> AA, etc."""
        result = ""
        while n >= 0:
            result = chr(n % 26 + ord("A")) + result
            n = n // 26 - 1
        return result
