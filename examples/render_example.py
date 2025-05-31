import json
from pathlib import Path

from AkvoFormPrint.stylers.weasyprint_styler import WeasyPrintStyler

# Define paths
FLOW_FORM_JSON_PATH = Path("examples/flow_form.json")
ARF_FORM_JSON_PATH = Path("examples/arf_form.json")
ANU_FORM_JSON_PATH = Path("examples/anu_form.json")
DEFAULT_FORM_JSON_PATH = Path("examples/default_form.json")
OUTPUT_HTML_PATH = Path("output/output_form.html")
OUTPUT_PDF_PATH = Path("output/output_form.pdf")


def render_form(
    input_path: Path,
    parser_type: str = "default",
    orientation: str = "landscape",
    add_section_numbering: bool = True,
):
    """Render a form to HTML and PDF.

    Args:
        input_path: Path to the form JSON file
        parser_type: Type of parser to use ("flow", "arf", or "default")
        orientation: Page orientation ("landscape" or "portrait")
        add_section_numbering: Whether to add section letters
    """
    # Create output directory
    OUTPUT_HTML_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Load form data
    with open(input_path, "r", encoding="utf-8") as f:
        form_json = json.load(f)

    # Initialize styler with all configuration
    styler = WeasyPrintStyler(
        orientation=orientation,
        add_section_numbering=add_section_numbering,
        parser_type=parser_type,
        raw_json=form_json,
    )

    # Render and save HTML
    html_content = styler.render_html()
    OUTPUT_HTML_PATH.write_text(html_content, encoding="utf-8")
    print(f"HTML saved to {OUTPUT_HTML_PATH}")

    # Render and save PDF
    pdf_content = styler.render_pdf()
    OUTPUT_PDF_PATH.write_bytes(pdf_content)
    print(f"PDF saved to {OUTPUT_PDF_PATH}")


def main():
    # Example: Render ANU form with flow parser
    render_form(
        input_path=ANU_FORM_JSON_PATH,
        parser_type="flow",
        orientation="landscape",
        add_section_numbering=True,
    )

    # Example: Render ARF form with arf parser
    # render_form(
    #     input_path=ARF_FORM_JSON_PATH,
    #     parser_type="arf",
    #     orientation="portrait",
    # )

    # Example: Render flow form with default parser
    # render_form(
    #     input_path=DEFAULT_FORM_JSON_PATH,
    #     add_section_numbering=False,
    # )


if __name__ == "__main__":
    main()
