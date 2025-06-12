# AkvoFormPrint

AkvoFormPrint is a flexible Python-based rendering engine designed to convert structured digital forms into styled HTML and PDF documents. It provides a robust solution for:
- Converting digital form definitions into printable formats
- Supporting multiple form schemas (Akvo Flow, ARF, Webform, custom JSON)
- Handling complex form features like dependencies and validation
- Generating professional, print-ready documents

## Table of Contents

- [AkvoFormPrint](#akvoformprint)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
    - [System Dependencies](#system-dependencies)
    - [Python Package Installation](#python-package-installation)
    - [Troubleshooting](#troubleshooting)
  - [Quick Start](#quick-start)
  - [Form Formats](#form-formats)
    - [Default Format](#default-format)
    - [Akvo Flow Format](#akvo-flow-format)
    - [Akvo Webform Format](#akvo-webform-format)
    - [ARF Format](#arf-format)
    - [Supported Question Types](#supported-question-types)
  - [Development](#development)
    - [Setup](#setup)
    - [Examples](#examples)

## Features

- Convert form definitions to **PDF**, **HTML** or **DOCX** with professional styling
- Support for multiple form formats:
  - Default JSON format for custom implementations
  - Akvo Flow forms (compatible with Flow's form structure)
  - Akvo Webform format
  - Akvo React Forms (ARF) with advanced validation
- **WeasyPrint Styler for rendering PDF and HTML**:
  - Portrait/landscape orientation for different form needs
  - Automatic section lettering (A, B, C) and question numbering
  - Custom templates for branded outputs (only for HTML and PDF)
  - Clean and modern form layout with responsive design
- **DOCX Rendering**:
  - Generate Microsoft Word documents (DocxRenderer) with:
  - Portrait/landscape orientation.
  - Automatic section lettering (A, B, C) and question numbering.
  - Multi-column layouts for option-based questions.

## Installation

### System Dependencies

AkvoFormPrint uses WeasyPrint for PDF generation, which requires system-level graphics and text rendering libraries. These must be installed before installing the Python package:

For Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libffi-dev \
    libxml2 \
    libxslt1.1 \
    shared-mime-info \
    fonts-liberation \
    fonts-dejavu-core
```

For macOS:
```bash
brew install pango
brew install libffi
brew install cairo
brew install fontconfig
```

### Python Package Installation

After installing the system dependencies above, you can install AkvoFormPrint:

```bash
pip install AkvoFormPrint
```

### Troubleshooting

Common issues and solutions:

1. System Dependencies Error:
```
OSError: cannot load library 'libgobject-2.0-0': libgobject-2.0-0: cannot open shared object file: No such file or directory
```
Solution: Install the required system dependencies as shown above.

2. PDF Generation Issues:
If you encounter problems with PDF generation, ensure all system dependencies are properly installed.

## Quick Start

```python
from AkvoFormPrint.stylers.weasyprint_styler import WeasyPrintStyler
from AkvoFormPrint.stylers.docx_renderer import DocxRenderer

# Your form data in the default format
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
                    "required": True
                }
            ]
        }
    ]
}

# Initialize styler with appropriate parser
styler = WeasyPrintStyler(
    orientation="portrait",
    add_section_numbering=True,
    add_question_numbering=True,
    parser_type="default",  # Options: "flow", "arf", "default"
    raw_json=form_json
)

# Generate HTML
html_content = styler.render_html()
with open("form.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# Generate PDF
pdf_content = styler.render_pdf()
with open("form.pdf", "wb") as f:
    f.write(pdf_content)

# DOCX Renderer
renderer = DocxRenderer(
    orientation="portrait",          # or "landscape"
    add_section_numbering=True,      # Enable section letters (A, B, C)
    add_question_numbering=True,     # Enable question numbers
    parser_type="default",           # "flow", "arf", or "default"
    raw_json=form_json,              # Form JSON
    output_path="form_output.docx"   # Output file
)
renderer.render_docx()
```

## Form Formats

AkvoFormPrint supports multiple form formats through different parsers:

### Default Format

The simplest format, used for custom implementations:

```json
{
  "title": "Your Form Title",
  "sections": [
    {
      "title": "Section Title",
      "questions": [
        {
          "id": "q1",
          "type": "input",
          "label": "Question text",
          "required": false,
          "options": [],
          "allowOther": false,
          "optionSingleLine": false,
          "minValue": null,
          "maxValue": null,
          "dependencies": [
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

### Akvo Flow Format

Compatible with Akvo Flow's form structure. Use `parser_type="flow"`:

```json
{
  "name": "Form Title",
  "questionGroup": [
    {
      "heading": "Section Title",
      "question": [
        {
          "id": "q1",
          "text": "Question text",
          "type": "free",
          "mandatory": true,
          "dependency": {
            "answer-value": "Yes",
            "question": "q2"
          }
        }
      ]
    }
  ]
}
```

### Akvo Webform Format

Similar to Flow format but with slightly different dependency structure. Uses the Flow parser:

```json
{
  "name": "Form Title",
  "questionGroup": [
    {
      "heading": "Section Title",
      "question": [
        {
          "id": "q1",
          "text": "Question text",
          "type": "free",
          "mandatory": true,
          "dependency": [
            {
              "answerValue": ["Yes"],
              "question": "q2"
            }
          ]
        }
      ]
    }
  ]
}
```

### ARF Format

For Akvo React Forms. Use `parser_type="arf"`:

```json
{
  "name": "Form Title",
  "question_group": [
    {
      "name": "Section Title",
      "question": [
        {
          "id": "q1",
          "name": "Question text",
          "type": "input",
          "required": true
        }
      ]
    }
  ]
}
```

### Supported Question Types

Each question type is designed to handle specific input needs:

- `input`: Single-line text input for short answers
- `number`: Numeric input with optional min/max validation
- `text`: Multi-line text input for longer responses
- `date`: Date input with format validation
- `option`: Single choice from a list of options
- `multiple_option`: Multiple choice selection
- `image`: Image upload and preview
- `geo`: Geographic coordinates with map support
- `cascade`: Hierarchical selection (e.g., Country > State > City)
- `table`: Grid-based data entry
- `autofield`: System-generated values
- `tree`: Tree-structured selection
- `signature`: Digital signature capture

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/akvo/akvo-form-print.git
cd akvo-form-print
```

2. Using Docker:

```bash
# Run development server with auto-reload
docker compose up dev

# Run specific examples
docker compose up basic   # Basic example
docker compose up flow    # Flow form example
docker compose up arf     # ARF form example
docker compose up webform # Akvo webform form example
docker compose up custom  # Custom styling example

# Run all examples
docker compose up examples

# Run tests
docker compose up test
```

3. Local Development:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in editable mode
pip install -e .

# Run tests
./run_tests.sh
```

### Examples

The `examples/` directory contains practical demonstrations:

- `basic_example.py`: Shows basic usage with the default parser
- `flow_example.py`: Demonstrates Akvo Flow form rendering
- `webform_example.py`: Demonstrates Akvo Webform form rendering
- `arf_example.py`: Shows ARF form rendering capabilities
- `custom_example.py`: Illustrates styling customization options

Each example is documented and shows different features. See `examples/README.md` for detailed explanations.

