#!/bin/bash

set -e

LIB_NAME="AkvoFormPrint"
VERSION_FILE="./src/AkvoFormPrint/__init__.py"
CHANGELOG_FILE="CHANGELOG.md"
CURRENT_VERSION=$(< $VERSION_FILE tr ' ' _ \
    | grep __version__ \
    | cut -d "=" -f2 \
    | sed 's/"//g' \
    | sed 's/_/v/g'
)

# Function to validate version format
validate_version() {
    local version=$1
    if [[ ! $version =~ ^[0-9]+\.[0-9]+\.[0-9]+(a|b|rc)?[0-9]*$ ]]; then
        echo "Invalid version format. Expected format: X.Y.Z[aN|bN|rcN] (e.g., 0.1.0, 0.1.0a1, 1.0.0rc1)"
        return 1
    fi
    return 0
}

# Function to update version in __init__.py
update_version() {
    local new_version=$1
    sed -i.bak "s/__version__ = \".*\"/__version__ = \"$new_version\"/" $VERSION_FILE
    rm -f "${VERSION_FILE}.bak"
    echo "Version updated to $new_version"
}

# Function to generate changelog entry
generate_changelog() {
    local version=$1
    local date=$(date +%Y-%m-%d)
    local temp_changelog=$(mktemp)

    # Get commit messages since last tag
    local last_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
    local log_range=${last_tag:+"$last_tag..HEAD"}

    {
        echo "# Changelog"
        echo
        echo "## [$version] - $date"
        echo
        if [ -n "$last_tag" ]; then
            echo "### Changes since $last_tag"
            echo
            git log $log_range --pretty=format:"* %s" --no-merges | while read -r line; do
                echo "$line"
            done
        else
            echo "### Initial Release"
            echo
            git log --pretty=format:"* %s" --no-merges | while read -r line; do
                echo "$line"
            done
        fi
        echo
        if [ -f "$CHANGELOG_FILE" ]; then
            echo
            tail -n +2 "$CHANGELOG_FILE"  # Skip the first line (# Changelog)
        fi
    } > "$temp_changelog"

    mv "$temp_changelog" "$CHANGELOG_FILE"
    echo "Changelog updated for version $version"
}

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

# Interactive version update
echo "Current version: $CURRENT_VERSION"
read -p "Do you want to update the version? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    while true; do
        read -p "Enter new version: " NEW_VERSION
        if validate_version "$NEW_VERSION"; then
            update_version "$NEW_VERSION"
            CURRENT_VERSION=$NEW_VERSION
            break
        fi
    done
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

# Generate changelog
generate_changelog "$CURRENT_VERSION"

# Commit version and changelog updates
git add "$VERSION_FILE" "$CHANGELOG_FILE"
git commit -m "Release $CURRENT_VERSION"
git push "${REPO_URL}" main

# Build and upload to PyPI
build_and_upload

# Create git tag and push
git tag -a "$CURRENT_VERSION" -m "Release $CURRENT_VERSION"
git push "${REPO_URL}" "$CURRENT_VERSION"

# Create GitHub release using the REST API
CHANGELOG_CONTENT=$(awk "/## \[$CURRENT_VERSION\]/,/## \[/" "$CHANGELOG_FILE" | sed '/## \[/d' | sed 's/"/\\"/g')

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
    \"body\":\"${CHANGELOG_CONTENT}\",
    \"draft\":false,
    \"prerelease\":false,
    \"generate_release_notes\":true
  }"

echo "Release completed successfully!"