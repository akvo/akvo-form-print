# AkvoFormPrint

**AkvoFormPrint** is a flexible Python-based rendering engine designed to convert structured digital forms into styled HTML and PDF documents. It supports form parsing, dependency mapping, and layout styling — making it suitable for surveys, assessments, and custom form tools like Akvo Flow or other JSON-based form formats.

---

## Table of Contents

- [AkvoFormPrint](#akvoformprint)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
    - [Using Docker (Recommended)](#using-docker-recommended)
    - [Run Tests](#run-tests)
    - [Development Setup (Without Docker)](#development-setup-without-docker)
  - [Usage](#usage)
    - [Basic Usage](#basic-usage)
    - [Supported Form Types](#supported-form-types)
    - [Default Form Format](#default-form-format)
    - [Configuration Options](#configuration-options)
  - [Examples](#examples)

---

## Features

* ✅ Parse structured form definitions (e.g., from Akvo Flow, Akvo React Form, or custom schemas)
* ✅ Standard JSON format for custom form implementations
* ✅ Automatically inject section and question numbers (e.g., `A.1`, `B.2`)
* ✅ Supports conditional logic and dependencies between questions
* ✅ Customizable HTML templates using **Jinja2**
* ✅ Generates printable PDFs using **WeasyPrint**
* ✅ Multiple form parsers with automatic format detection
* ✅ Configurable page orientation and section numbering
* ✅ Designed for extensibility and reusability

---

## Project Structure

```
.
├── docker-compose.yml         # Docker configuration
├── Dockerfile                 # Container build instructions
├── examples/                  # Example form files and render script
├── output/                    # HTML and PDF output
├── src/AkvoFormPrint/         # Core modules (models, parsers, stylers)
├── tests/                     # Pytest-based test suite
├── templates/ & styles/       # Jinja2 templates and CSS for layout
├── requirements.txt          # Python dependencies
└── README.md
```

---

## Getting Started

### Using Docker (Recommended)

To build and run the application:

```bash
docker compose up --build
```

This will render example forms and generate outputs in the `output/` directory.

### Run Tests

To run tests using Docker:

```bash
docker compose run test
```

To run tests locally:

```bash
pytest tests/
```

### Development Setup (Without Docker)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

### Basic Usage

```python
from AkvoFormPrint.stylers.weasyprint_styler import WeasyPrintStyler

# Load your form data
with open("form_data.json", "r") as f:
    form_json = json.load(f)

# Create styler with configuration
styler = WeasyPrintStyler(
    orientation="landscape",
    add_section_numbering=True,
    parser_type="default",  # or "flow" or "arf"
    raw_json=form_json
)

# Generate HTML
html_content = styler.render_html()

# Generate PDF
pdf_content = styler.render_pdf()
```

### Supported Form Types

The library supports three form types through different parsers:

1. **Default Parser** (`parser_type="default"`):
   - Standard format for custom implementations
   - Simple, flat form structure
   - Sections with questions
   - Basic question types and dependencies

2. **Akvo Flow Parser** (`parser_type="flow"`):
   - Compatible with Akvo Flow form format
   - Supports complex question types
   - Handles cascading questions and dependencies

3. **Akvo React Form Parser** (`parser_type="arf"`):
   - Supports Akvo React Form format
   - Advanced validation rules
   - Variable name mapping

### Default Form Format

If you have a custom form schema and don't want to create a new parser, you can transform your data to match the default JSON format:

```json
{
  "title": "Your Form Title",
  "sections": [
    {
      "title": "Section Title",
      "questions": [
        {
          "id": "q1",
          "type": "input",  // See supported types below
          "label": "Question text",
          "required": false,
          "options": [],    // For option/multiple_option types
          "allowOther": false,  // For option types
          "optionSingleLine": false,
          "minValue": null,  // For number type
          "maxValue": null,  // For number type
          "dependencies": [  // Optional question dependencies
            {
              "depends_on_question_id": "q2",
              "expected_answer": "Yes"
            }
          ]
        }
      ]
    }
  ]
}
```

Supported question types:
- `input`: Text input
- `number`: Numeric input with optional min/max
- `text`: Multi-line text
- `date`: Date input
- `option`: Single choice from options
- `multiple_option`: Multiple choice from options
- `image`: Image upload
- `geo`: Geographic coordinates
- `cascade`: Cascading select
- `table`: Table input
- `autofield`: Auto-generated field
- `tree`: Tree select
- `signature`: Signature input

This format serves as the standard interface for the library. Instead of creating a custom parser, you can transform your form data to match this structure and use the default parser.

### Configuration Options

The `WeasyPrintStyler` accepts the following configuration options:

- `orientation`: Page orientation ("landscape" or "portrait")
- `add_section_numbering`: Whether to add section letters (A, B, C, etc.)
- `parser_type`: Type of parser to use ("default", "flow", or "arf")
- `raw_json`: Form data to parse

---

## Examples

You can test the rendering functionality using provided examples:

```python
# Example 1: Default form with landscape orientation
render_form(
    input_path="examples/default_form.json",
    add_section_numbering=True
)

# Example 2: Flow form with portrait orientation
render_form(
    input_path="examples/flow_form.json",
    parser_type="flow",
    orientation="portrait"
)

# Example 3: ARF form with custom configuration
render_form(
    input_path="examples/arf_form.json",
    parser_type="arf",
    orientation="landscape",
    add_section_numbering=False
)
```

Run the example script:
```bash
python examples/render_example.py
```

This will generate:
* `output/output_form.html`
* `output/output_form.pdf`

