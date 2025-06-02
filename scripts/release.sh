#!/bin/bash

set -e

git checkout main
git pull
git fetch --tags

LIB_NAME="AkvoFormPrint"
CURRENT_VERSION=$(< ./src/AkvoFormPrint/__init__.py tr ' ' _ \
    | grep __version__ \
    | cut -d "=" -f2 \
    | sed 's/"//g' \
    | sed 's/_/v/g'
)
CURRENT_TAG=$(git describe --abbrev=0 2>/dev/null || echo "no_tag")

if [[ "$CURRENT_VERSION" == "$CURRENT_TAG" ]]; then
    printf "Please modify version\n"
    printf "Located at ./src/AkvoFormPrint/__init__.py\n"
    printf "Latest Release: %s %s\n" "$LIB_NAME" "$CURRENT_TAG"
    exit 0
fi

# Configure git to use HTTPS with token
if [ -n "$GITHUB_TOKEN" ]; then
    git config --global url."https://api:${GITHUB_TOKEN}@github.com/".insteadOf "https://github.com/"
    git config --global url."https://ssh:${GITHUB_TOKEN}@github.com/".insteadOf "ssh://git@github.com/"
    git config --global url."https://git:${GITHUB_TOKEN}@github.com/".insteadOf "git@github.com:"
fi

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
    if [[ $CURRENT_VERSION == *"a"* ]] || [[ $CURRENT_VERSION == *"b"* ]] || [[ $CURRENT_VERSION == *"rc"* ]]; then
        echo "Uploading to Test PyPI..."
        python -m twine upload --repository testpypi dist/*
    else
        echo "Uploading to PyPI..."
        python -m twine upload dist/*
    fi
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

# Configure git user
git config --global user.email "tech.consultancy@akvo.org"
git config --global user.name "Akvo Tech Consultancy"

# Build and upload to PyPI
build_and_upload

# Create git tag and push
git tag -a "$CURRENT_VERSION" -m "Release $CURRENT_VERSION"
git push origin "$CURRENT_VERSION"

# Create GitHub release using gh CLI
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