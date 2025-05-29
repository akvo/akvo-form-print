from setuptools import setup, find_packages

setup(
    name="AkvoFormPrint",
    version="0.1.0a0",  # alpha version
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "weasyprint",
        "jinja2",
    ],
    author="Akvo",
    description=(
        """Render modular forms into PDF or HTML
        using WeasyPrint with custom templates and styling."""
    ),
    include_package_data=True,
)
