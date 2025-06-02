"""
Example showing how to use AkvoFormPrint with Akvo React Forms (ARF).
"""

import json
from pathlib import Path

from AkvoFormPrint.stylers.weasyprint_styler import WeasyPrintStyler

# Define paths
DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    # Load ARF form data
    with open(DATA_DIR / "arf_form.json", "r", encoding="utf-8") as f:
        arf_json = json.load(f)

    # Initialize styler with ARF parser
    styler = WeasyPrintStyler(
        orientation="portrait",
        add_section_numbering=True,
        parser_type="arf",
        raw_json=arf_json,
    )

    # Generate HTML
    html_content = styler.render_html()
    html_path = OUTPUT_DIR / "arf_form.html"
    html_path.write_text(html_content, encoding="utf-8")
    print(f"HTML saved to {html_path}")

    # Generate PDF
    pdf_content = styler.render_pdf()
    pdf_path = OUTPUT_DIR / "arf_form.pdf"
    pdf_path.write_bytes(pdf_content)
    print(f"PDF saved to {pdf_path}")


if __name__ == "__main__":
    main()
