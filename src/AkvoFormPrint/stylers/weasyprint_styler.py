from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from typing import Any, Dict, Optional

from AkvoFormPrint.parsers.akvo_flow_parser import AkvoFlowFormParser
from AkvoFormPrint.parsers.akvo_arf_parser import AkvoReactFormParser
from AkvoFormPrint.parsers.default_parser import DefaultParser
from AkvoFormPrint.parsers.base_parser import BaseParser


class WeasyPrintStyler:
    def __init__(
        self,
        orientation: str = "landscape",
        add_section_numbering: bool = False,
        parser_type: Optional[str] = None,
        raw_json: Optional[Dict[str, Any]] = None,
    ):
        """Initialize WeasyPrintStyler with all configuration parameters.

        Args:
            orientation: Page orientation. Defaults to "landscape".
            add_section_numbering: Add section letters. Defaults to False.
            parser_type: Type of parser ("flow", "arf", "default"). None.
            raw_json: Form data to parse. Defaults to None.
        """
        assert orientation in (
            "portrait",
            "landscape",
        ), "Orientation must be 'portrait' or 'landscape'"

        self.orientation = orientation
        self.add_section_numbering = add_section_numbering
        self.parser_type = parser_type
        self.raw_json = raw_json
        self.parser = None
        self.form_model = None

        # Initialize parser if we have config
        if parser_type or raw_json:
            self.parser = self._get_parser(parser_type)

        # Setup Jinja environment
        templates_path = Path(__file__).parent.parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(templates_path)))

        # Load CSS content once
        css_path = Path(__file__).parent.parent / "styles" / "default.css"
        self.css_content = css_path.read_text(encoding="utf-8")

        # Parse form if raw_json is provided
        if self.raw_json:
            self.form_model = self._parse_form()

    def _parse_form(self):
        """Parse form data using configured parser."""
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
            else:
                section.letter = None
            section_index += 1
            for question in section.questions:
                question.number = counter
                counter += 1
        return form

    def _get_parser(self, parser_type: Optional[str] = None) -> BaseParser:
        if parser_type == "flow":
            return AkvoFlowFormParser()
        elif parser_type == "arf":
            return AkvoReactFormParser()
        elif parser_type is None or parser_type == "default":
            return DefaultParser()
        else:
            raise ValueError(f"Unknown parser type: {parser_type}")

    def render_html(self) -> str:
        """Render form as HTML string using initialized configuration."""
        if not self.form_model:
            self.form_model = self._parse_form()

        template = self.env.get_template("form_template.html")
        return template.render(
            form=self.form_model,
            css_content=self.css_content + self._get_page_css(),
            orientation=self.orientation,
        )

    def render_pdf(self) -> bytes:
        """Render form as PDF bytes using initialized configuration."""
        html_content = self.render_html()
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
