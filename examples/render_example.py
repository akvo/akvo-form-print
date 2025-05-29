import json
from pathlib import Path

from AkvoFormPrint.parsers.akvo_flow_parser import AkvoFlowFormParser
from AkvoFormPrint.stylers.weasyprint_styler import WeasyPrintStyler

FORM_JSON_PATH = Path("examples/sample4_form.json")
OUTPUT_HTML_PATH = Path("output/output_form.html")
OUTPUT_PDF_PATH = Path("output/output_form.pdf")


def main():
    with open(FORM_JSON_PATH, "r", encoding="utf-8") as f:
        form_json = json.load(f)

    parser = AkvoFlowFormParser()
    form_model = parser.parse(form_json)

    print(f"Parsed form title: {form_model.title}")
    print(f"Number of sections: {len(form_model.sections)}")

    styler = WeasyPrintStyler(orientation="landscape")

    OUTPUT_HTML_PATH.parent.mkdir(parents=True, exist_ok=True)

    html_content = styler.render_html(form_model)
    OUTPUT_HTML_PATH.write_text(html_content, encoding="utf-8")
    print(f"HTML saved to {OUTPUT_HTML_PATH}")

    pdf_content = styler.render_pdf(form_model)
    OUTPUT_PDF_PATH.write_bytes(pdf_content)
    print(f"PDF saved to {OUTPUT_PDF_PATH}")


if __name__ == "__main__":
    main()
