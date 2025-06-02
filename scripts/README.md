# Release Process Documentation

This document describes the Docker-based release process for AkvoFormPrint.

## Project Setup Components

1. **Version Management**
   - Location: `src/AkvoFormPrint/__init__.py`
   - Manages package version using `__version__` variable
   - Version is read by `setup.cfg` during build
   - Interactive version update during release process

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
   - Runs inside a Docker container for consistency
   - Generates changelog automatically
   - Creates GitHub releases using GitHub API

## Prerequisites

1. **Docker**
   - Install Docker on your system
   - Ensure docker-compose is available

2. **Environment Variables**
   You need to set up the following environment variables. There are two ways to do this:

   **Option 1: Set environment variables directly**
   ```bash
   # GitHub Personal Access Token with repo scope
   export GITHUB_TOKEN="your-github-token"

   # PyPI API Token
   export PYPI_TOKEN="your-pypi-token"

   # Git Configuration
   export GIT_USER_NAME="your-git-username"
   export GIT_USER_EMAIL="your-git-email"
   ```

   **Option 2: Use a .env file (Recommended)**
   1. Copy the example environment file:
      ```bash
      cp env_example .env
      ```

   2. Edit the `.env` file with your values:
      ```ini
      GIT_USER_NAME=your-git-username
      GIT_USER_EMAIL=your-git-email
      PYPI_TOKEN=your-pypi-token
      GITHUB_TOKEN=your-github-token
      ```

   To get these tokens:
   - GitHub Token: Visit https://github.com/settings/tokens and create a token with 'repo' scope
   - PyPI Token: Visit https://pypi.org/manage/account/token/ and create an API token
   - Git Config: Use your GitHub username and email address

   Note: The `.env` file is already in `.gitignore` to prevent accidentally committing sensitive information.

## Release Process

1. Update version in `src/AkvoFormPrint/__init__.py` (Optional):
   ```python
   __version__ = "X.Y.Z"    # For releases (e.g., "0.1.0", "1.0.0")
   __version__ = "X.Y.ZaN"  # For alpha versions (e.g., "0.1.0a1")
   __version__ = "X.Y.ZbN"  # For beta versions (e.g., "0.1.0b1")
   __version__ = "X.Y.ZrcN" # For release candidates (e.g., "0.1.0rc1")
   ```
   Note: The release script will interactively ask if you want to update the version.

2. Run the release process:
   ```bash
   docker compose run --rm release
   ```

   Or if you're setting environment variables directly (without .env file):
   ```bash
   docker compose run --rm \
     -e GITHUB_TOKEN="your-github-token" \
     -e PYPI_TOKEN="your-pypi-token" \
     -e GIT_USER_NAME="your-git-username" \
     -e GIT_USER_EMAIL="your-git-email" \
     release
   ```

The release process will automatically:
- Ask if you want to update the version
- Run comprehensive tests using tox
- Build the Python package
- Generate changelog from git commits
- Upload to PyPI
- Create a git tag
- Push changes to GitHub
- Create a GitHub release with changelog using GitHub API

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
   - Update the version number when prompted

2. **Tox Tests Fail**
   ```
   Tests failed. Aborting release.
   ```
   - Check the Docker logs for detailed error messages
   - Common issues:
     - Failed flake8 checks (style issues)
     - Failed black checks (formatting issues)
     - Failed check-manifest (missing files)
     - Failed tests in specific Python versions

3. **PyPI Upload Fails**
   - Check if PYPI_TOKEN is correctly set
   - Ensure token has upload permissions
   - Version number not already used
   - Check network connection

4. **GitHub Release Fails**
   - Check if GITHUB_TOKEN is correctly set
   - Ensure token has repo scope permissions
   - Check network connection
   - Verify curl is installed in the container

## Development Workflow

1. Development Phase (Alpha):
   - Use alpha versions (0.1.0a1, 0.1.0a2, etc.)
   - Run tests with `docker compose run --rm test`
   - Share with early adopters

2. Testing Phase (Beta):
   - Use beta versions (0.1.0b1, 0.1.0b2, etc.)
   - More stable features
   - Full test coverage

3. Pre-release Phase (RC):
   - Use release candidates (0.1.0rc1, 0.1.0rc2, etc.)
   - Feature freeze
   - All tests must pass

4. Release Phase:
   - Use final version numbers (0.1.0, 1.0.0, etc.)
   - All tests must pass
   - Ready for general use

## Container Details

The release process uses a Docker container defined in `Dockerfile.release` which:
- Uses Python 3.10 slim as the base image
- Installs required system dependencies (WeasyPrint, git, curl)
- Sets up the build environment
- Configures git for HTTPS operations
- Handles the entire release process in an isolated environment

This containerized approach ensures:
- Consistent build environment
- Reproducible releases
- No dependency conflicts with local system
- Simplified release process
- Automated changelog generation