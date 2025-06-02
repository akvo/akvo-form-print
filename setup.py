from setuptools import setup, find_packages

short_description = "Render modular forms into PDF or HTML using WeasyPrint"
short_description += " with custom templates and styling"

setup(
    name="AkvoFormPrint",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "weasyprint>=60.1",
        "jinja2>=3.1.3",
    ],
    python_requires=">=3.8",
    author="Akvo",
    author_email="tech.consultancy@akvo.org",
    maintainer="Wayan Galih Pratama",
    maintainer_email="wgprtm@gmail.com",
    description=short_description,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/akvo/akvo-form-print",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="form, pdf, html, weasyprint, akvo",
    project_urls={
        "Bug Reports": "https://github.com/akvo/akvo-form-print/issues",
        "Source": "https://github.com/akvo/akvo-form-print",
        "Organization": "https://github.com/akvo",
    },
    include_package_data=True,
)
