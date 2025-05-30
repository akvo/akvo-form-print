import json
from pathlib import Path

from AkvoFormPrint.stylers.weasyprint_styler import WeasyPrintStyler

FLOW_FORM_JSON_PATH = Path("examples/flow_form.json")
ARF_FORM_JSON_PATH = Path("examples/arf_form.json")
ANU_FORM_JSON_PATH = Path("examples/anu_form.json")
OUTPUT_HTML_PATH = Path("output/output_form.html")
OUTPUT_PDF_PATH = Path("output/output_form.pdf")
PARSER_TYPE = "flow"


# TODO :: Default json schema from models
def main():
    with open(ANU_FORM_JSON_PATH, "r", encoding="utf-8") as f:
        form_json = json.load(f)

    styler = WeasyPrintStyler(orientation="landscape")

    OUTPUT_HTML_PATH.parent.mkdir(parents=True, exist_ok=True)

    html_content = styler.render_html(form_json, PARSER_TYPE)
    OUTPUT_HTML_PATH.write_text(html_content, encoding="utf-8")
    print(f"HTML saved to {OUTPUT_HTML_PATH}")

    pdf_content = styler.render_pdf(form_json, PARSER_TYPE)
    OUTPUT_PDF_PATH.write_bytes(pdf_content)
    print(f"PDF saved to {OUTPUT_PDF_PATH}")


if __name__ == "__main__":
    main()
