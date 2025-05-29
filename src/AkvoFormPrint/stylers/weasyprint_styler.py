from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS


class WeasyPrintStyler:
    def __init__(self, orientation: str = "landscape"):
        assert orientation in (
            "portrait",
            "landscape",
        ), "Orientation must be 'portrait' or 'landscape'"
        self.orientation = orientation

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
            section.letter = self._number_to_letter(section_index)
            section_index += 1
            for question in section.questions:
                question.number = counter
                counter += 1
        return form

    def render_html(self, form):
        form = self.inject_question_numbers(form)
        template = self.env.get_template("form_template.html")
        return template.render(
            form=form,
            css_content=self.css_content + self._get_page_css(),
            orientation=self.orientation,
        )

    def render_pdf(self, form) -> bytes:
        form = self.inject_question_numbers(form)
        html_content = self.render_html(form)
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
