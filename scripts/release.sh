#!/bin/bash

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

function push_release() {
    # GitHub CLI api
    # https://cli.github.com/manual/gh_api
    gh api \
        --method POST \
        -H "Accept: application/vnd.github+json" \
        "/repos/akvo/akvo-form-print/releases" \
        -f tag_name="$1" \
        -f target_commitish='main' \
        -f name="$LIB_NAME $1" \
        -f body="$(printf "%s" "$2")" \
        -F draft=false \
        -F prerelease=false \
        -F generate_release_notes=false
}

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

if [[ $# -eq 0 ]]; then
    printf "Please write description\n"
    read -r DESC
    printf "Release: %s %s\n" "$LIB_NAME" "$CURRENT_VERSION"

    # Build and upload to PyPI
    build_and_upload

    # Create git tag and release
    git tag -a "$CURRENT_VERSION" -m "New Release $CURRENT_VERSION: $DESC"
    git push --tags
    printf "%s" "${DESC}"
    push_release "${CURRENT_VERSION}" "${DESC}"
fi