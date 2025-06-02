# Release Process Documentation

This document describes the release process for AkvoFormPrint using our automated setup.

## Project Setup Components

1. **Version Management**
   - Location: `src/AkvoFormPrint/__init__.py`
   - Manages package version using `__version__` variable
   - Version is read by `setup.cfg` during build

2. **Build Configuration**
   - Location: `setup.cfg`
   - Contains package metadata
   - Configures tools (flake8, black)
   - References version from `AkvoFormPrint.__version__`

3. **Test Automation**
   - Location: `tox.ini`
   - Runs tests across Python versions (3.8-3.11)
   - Integrates flake8 and black checks
   - Runs check-manifest for package completeness
   - Generates coverage reports

4. **Release Automation**
   - Location: `scripts/release.sh`
   - Automates the entire release process
   - Handles versioning, testing, and deployment

## Prerequisites

1. Install required tools:
```bash
pip install build twine tox check-manifest
```

2. Install GitHub CLI:
```bash
# macOS
brew install gh

# Linux
# See: https://github.com/cli/cli/blob/trunk/docs/install_linux.md
```

3. Set up PyPI authentication:
   - Create an account on PyPI if you haven't: https://pypi.org/account/register/
   - Generate an API token: https://pypi.org/manage/account/token/
   - Create or edit `~/.pypirc` in your home directory (NOT in the project directory):
```ini
[pypi]
username = __token__
password = your-pypi-token-here
```
   - Ensure proper file permissions:
```bash
chmod 600 ~/.pypirc
```
   - NEVER commit `.pypirc` to version control
   - NEVER share your PyPI token

4. Login to GitHub CLI:
```bash
gh auth login
```

## Release Process

1. Update version in `src/AkvoFormPrint/__init__.py`:
```python
__version__ = "X.Y.Z"    # For releases (e.g., "0.1.0", "1.0.0")
__version__ = "X.Y.ZaN"  # For alpha versions (e.g., "0.1.0a1")
__version__ = "X.Y.ZbN"  # For beta versions (e.g., "0.1.0b1")
__version__ = "X.Y.ZrcN" # For release candidates (e.g., "0.1.0rc1")
```

2. Run the release script:
```bash
./scripts/release.sh
```

The script will automatically:
- Verify the version has been updated from the last release
- Run comprehensive tests using tox:
  - Python version compatibility (3.8-3.11)
  - Code style (flake8)
  - Code formatting (black)
  - Package completeness (check-manifest)
- Build the package using `setup.cfg` configuration
- Upload to PyPI
- Create a git tag
- Generate a GitHub release

## Version Numbering

We follow semantic versioning with pre-release designations:

- Alpha: `0.1.0a1`, `0.1.0a2`, etc.
  - Early development
  - Expect bugs and API changes
  - Suitable for early testing

- Beta: `0.1.0b1`, `0.1.0b2`, etc.
  - Feature complete
  - Testing and refinement
  - Suitable for wider testing

- Release Candidate: `0.1.0rc1`, `0.1.0rc2`, etc.
  - Potential final release
  - Final testing and bug fixes
  - Ready for production testing

- Final: `0.1.0`, `1.0.0`, etc.
  - Stable release
  - Production ready
  - Fully tested

## Troubleshooting

1. **Version Already Exists**
   ```
   Please modify version
   Located at ./src/AkvoFormPrint/__init__.py
   ```
   - The version in `__init__.py` matches an existing tag
   - Update the version number

2. **Tox Tests Fail**
   ```
   Tests failed. Aborting release.
   ```
   - Run `tox` manually to see detailed errors
   - Common issues:
     - Failed flake8 checks (style issues)
     - Failed black checks (formatting issues)
     - Failed check-manifest (missing files)
     - Failed tests in specific Python versions

3. **PyPI Upload Fails**
   - Check `~/.pypirc` configuration
   - Ensure token is valid
   - Version number not already used
   - Check network connection

4. **GitHub Release Fails**
   - Check GitHub CLI authentication
   - Ensure you have proper repository permissions
   - Check network connection

## Development Workflow

1. Development Phase (Alpha):
   - Use alpha versions (0.1.0a1, 0.1.0a2, etc.)
   - Run frequent tests with `tox`
   - Share with early adopters

2. Testing Phase (Beta):
   - Use beta versions (0.1.0b1, 0.1.0b2, etc.)
   - More stable features
   - Ensure all tox environments pass

3. Pre-release Phase (RC):
   - Use release candidates (0.1.0rc1, 0.1.0rc2, etc.)
   - Feature freeze
   - Full test coverage

4. Release Phase:
   - Use final version numbers (0.1.0, 1.0.0, etc.)
   - All tox environments must pass
   - Ready for general use