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
  - [Examples](#examples)
  - [Extensibility](#extensibility)
  - [Notes](#notes)
  - [Contributing](#contributing)
  - [License](#license)

---

## Features

* ✅ Parse structured form definitions (e.g., from Akvo Flow, Akvo React Form, or custom schemas)
* ✅ Automatically inject section and question numbers (e.g., `A.1`, `B.2`)
* ✅ Supports conditional logic and dependencies between questions
* ✅ Customizable HTML templates using **Jinja2**
* ✅ Generates printable PDFs using **WeasyPrint**
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
├── requirements.txt           # Python dependencies
├── pyproject.toml / setup.py  # Packaging and build configuration
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

---

### Run Tests

To run tests using Docker:

```bash
docker compose run test
```

To run tests locally:

```bash
pytest tests/
```

---

### Development Setup (Without Docker)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Examples

You can test the rendering functionality using provided examples:

```bash
python examples/render_example.py
```

This will generate:

* `output/output_form.html`
* `output/output_form.pdf`

---

## Extensibility

This project is designed to be extensible. You can:

* 🧹 Add custom **parsers** for other form formats (e.g., Akvo React Form)
* 🎨 Create new **stylers** to handle different numbering or visual rules
* 📝 Modify **Jinja2 templates** to adjust HTML structure
* 🔄 Customize the **dependency logic** for conditional question flows

The modular architecture makes it easy to swap or extend components for new use cases.

---

## Notes

* Akvo Flow form with variable names:
  `https://tech-consultancy.akvo.org/akvo-flow-web-api/seap/1178020913/update`
* Akvo Flow form without variable names:
  `https://webform.akvo.org/api/form/n5yztxxc6j4jqx22`

---

## Contributing

We welcome contributions! Whether it's bug fixes, parser support for new form types, or styling improvements — feel free to open a PR or issue.

---

## License

MIT License © Akvo Foundation
