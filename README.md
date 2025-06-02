# AkvoFormPrint

AkvoFormPrint is a flexible Python-based rendering engine designed to convert structured digital forms into styled HTML and PDF documents. It provides a robust solution for:
- Converting digital form definitions into printable formats
- Supporting multiple form schemas (Akvo Flow, ARF, custom JSON)
- Handling complex form features like dependencies and validation
- Generating professional, print-ready documents

## Table of Contents

- [AkvoFormPrint](#akvoformprint)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
  - [Form Format](#form-format)
    - [Supported Question Types](#supported-question-types)
  - [Development](#development)
    - [Setup](#setup)
    - [Examples](#examples)

## Features

- Convert form definitions to PDF or HTML with professional styling
- Support for multiple form formats:
  - Default JSON format for custom implementations
  - Akvo Flow forms (compatible with Flow's form structure)
  - Akvo React Forms (ARF) with advanced validation
- Customizable styling options:
  - Portrait/landscape orientation for different form needs
  - Automatic section lettering (A, B, C) and question numbering
  - Custom templates for branded outputs
- Clean and modern form layout with responsive design
- Comprehensive question type support with validation
- Handles complex form features:
  - Question dependencies
  - Input validation rules
  - Custom option layouts
  - File attachments

## Installation

```bash
pip install AkvoFormPrint
```

## Quick Start

```python
from AkvoFormPrint.stylers.weasyprint_styler import WeasyPrintStyler

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

# Initialize styler
styler = WeasyPrintStyler(
    orientation="portrait",
    add_section_numbering=True,
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
```

## Form Format

The default form format uses a simple JSON structure that can represent any form layout. This format serves as a standard interface - if you have a different form schema, you can transform it to match this structure:

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
docker compose up flow   # Flow form example
docker compose up arf    # ARF form example
docker compose up custom # Custom styling example

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
- `arf_example.py`: Shows ARF form rendering capabilities
- `custom_example.py`: Illustrates styling customization options

Each example is documented and shows different features. See `examples/README.md` for detailed explanations.

