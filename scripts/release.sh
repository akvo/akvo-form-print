#!/bin/bash

set -e

LIB_NAME="AkvoFormPrint"
CURRENT_VERSION=$(< ./src/AkvoFormPrint/__init__.py tr ' ' _ \
    | grep __version__ \
    | cut -d "=" -f2 \
    | sed 's/"//g' \
    | sed 's/_/v/g'
)

# Configure git
if [ -n "$GIT_USER_NAME" ] && [ -n "$GIT_USER_EMAIL" ]; then
    git config --global user.name "$GIT_USER_NAME"
    git config --global user.email "$GIT_USER_EMAIL"
fi

# Configure git to use HTTPS
git config --global url."https://github.com/".insteadOf git@github.com:
git config --global url."https://".insteadOf git://

# Set explicit HTTPS remote
REPO_URL="https://${GITHUB_TOKEN}@github.com/akvo/akvo-form-print.git"
git remote set-url origin "${REPO_URL}"

function build_and_upload() {
    # Clean previous builds
    rm -rf dist/ build/ *.egg-info

    # Run tests with tox
    if ! tox; then
        echo "Tests failed. Aborting release."
        exit 1
    fi

    # Build package
    python -m build

    if [ $? -ne 0 ]; then
        echo "Build failed. Aborting release."
        exit 1
    fi

    # Upload to PyPI
    echo "Uploading to PyPI..."
    python -m twine upload dist/*
}

# Main execution
echo "Starting release process for $LIB_NAME $CURRENT_VERSION"

# Check if PYPI_TOKEN is set
if [ -z "$TWINE_PASSWORD" ]; then
    echo "Error: PYPI_TOKEN environment variable is not set"
    exit 1
fi

# Check if GITHUB_TOKEN is set
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN environment variable is not set"
    exit 1
fi

# Pull latest changes
git pull "${REPO_URL}" main

# Build and upload to PyPI
build_and_upload

# Create git tag and push
git tag -a "$CURRENT_VERSION" -m "Release $CURRENT_VERSION"
git push "${REPO_URL}" "$CURRENT_VERSION"
git push "${REPO_URL}" main

# Create GitHub release using the REST API
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/akvo/akvo-form-print/releases \
  -d "{
    \"tag_name\":\"${CURRENT_VERSION}\",
    \"target_commitish\":\"main\",
    \"name\":\"${LIB_NAME} ${CURRENT_VERSION}\",
    \"body\":\"Release ${CURRENT_VERSION}\",
    \"draft\":false,
    \"prerelease\":false,
    \"generate_release_notes\":true
  }"

echo "Release completed successfully!"