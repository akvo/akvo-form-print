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

# Configure git
if [ -n "$GITHUB_TOKEN" ]; then
    # Configure git user if provided
    if [ -n "$GIT_USER_NAME" ] && [ -n "$GIT_USER_EMAIL" ]; then
        git config --global user.name "$GIT_USER_NAME"
        git config --global user.email "$GIT_USER_EMAIL"
    fi
else
    echo "Error: GITHUB_TOKEN is not set"
    exit 1
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

# Build and upload to PyPI
build_and_upload

# Create git tag and push using HTTPS
git tag -a "$CURRENT_VERSION" -m "Release $CURRENT_VERSION"
git push "https://${GITHUB_TOKEN}@github.com/akvo/akvo-form-print.git" "$CURRENT_VERSION"

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