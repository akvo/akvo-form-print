"""
Basic example showing how to use AkvoFormPrint with the default parser.
"""

from pathlib import Path

from AkvoFormPrint.stylers.weasyprint_styler import WeasyPrintStyler

# Define paths
DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    # Load sample form data
    form_json = {
        "title": "Sample Form",
        "sections": [
            {
                "title": "Personal Information",
                "questions": [
                    {
                        "id": "q1",
                        "type": "input",
                        "label": "What is your name?",
                        "required": True,
                    },
                    {
                        "id": "q2",
                        "type": "option",
                        "label": "Select your gender",
                        "options": ["Male", "Female", "Other"],
                        "allowOther": True,
                    },
                ],
            },
            {
                "title": "Additional Information",
                "questions": [
                    {
                        "id": "q3",
                        "type": "multiple_option",
                        "label": "Select your interests",
                        "options": ["Reading", "Sports", "Music", "Travel"],
                    }
                ],
            },
        ],
    }

    # Initialize styler with configuration
    styler = WeasyPrintStyler(
        orientation="portrait", add_section_numbering=True, raw_json=form_json
    )

    # Generate HTML
    html_content = styler.render_html()
    html_path = OUTPUT_DIR / "basic_form.html"
    html_path.write_text(html_content, encoding="utf-8")
    print(f"HTML saved to {html_path}")

    # Generate PDF
    pdf_content = styler.render_pdf()
    pdf_path = OUTPUT_DIR / "basic_form.pdf"
    pdf_path.write_bytes(pdf_content)
    print(f"PDF saved to {pdf_path}")


if __name__ == "__main__":
    main()
