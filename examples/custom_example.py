"""
Example showing how to use AkvoFormPrint with custom styling options.
"""

import json
from pathlib import Path

from AkvoFormPrint.stylers.weasyprint_styler import WeasyPrintStyler

# Define paths
DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    # Load default form data
    with open(DATA_DIR / "default_form.json", "r", encoding="utf-8") as f:
        form_json = json.load(f)

    # Example 1: Landscape with section numbering
    styler1 = WeasyPrintStyler(
        orientation="landscape", add_section_numbering=True, raw_json=form_json
    )

    html_content = styler1.render_html()
    html_path = OUTPUT_DIR / "custom_form_landscape.html"
    html_path.write_text(html_content, encoding="utf-8")
    print(f"Landscape HTML saved to {html_path}")

    pdf_content = styler1.render_pdf()
    pdf_path = OUTPUT_DIR / "custom_form_landscape.pdf"
    pdf_path.write_bytes(pdf_content)
    print(f"Landscape PDF saved to {pdf_path}")

    # Example 2: Portrait without section numbering
    styler2 = WeasyPrintStyler(
        orientation="portrait", add_section_numbering=False, raw_json=form_json
    )

    html_content = styler2.render_html()
    html_path = OUTPUT_DIR / "custom_form_portrait.html"
    html_path.write_text(html_content, encoding="utf-8")
    print(f"Portrait HTML saved to {html_path}")

    pdf_content = styler2.render_pdf()
    pdf_path = OUTPUT_DIR / "custom_form_portrait.pdf"
    pdf_path.write_bytes(pdf_content)
    print(f"Portrait PDF saved to {pdf_path}")


if __name__ == "__main__":
    main()
