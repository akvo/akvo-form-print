# AkvoFormPrint Examples

This directory contains examples of how to use the AkvoFormPrint package.

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install AkvoFormPrint:
```bash
pip install AkvoFormPrint
```

## Examples

### 1. Basic Form Rendering
`basic_example.py` - Shows how to render a simple form using the default parser.

### 2. Flow Form Rendering
`flow_example.py` - Shows how to render an Akvo Flow form.

### 3. ARF Form Rendering
`arf_example.py` - Shows how to render an Akvo React Form.

### 4. Custom Styling
`custom_example.py` - Shows how to use custom styling options.

## Sample Form Data

The `data/` directory contains sample form JSON files:
- `default_form.json` - Example form using the default format
- `flow_form.json` - Example Akvo Flow form
- `arf_form.json` - Example Akvo React form

## Running Examples

Each example can be run directly:

```bash
python basic_example.py
python flow_example.py
python arf_example.py
python custom_example.py
```

The examples will generate HTML and PDF files in the `output/` directory.