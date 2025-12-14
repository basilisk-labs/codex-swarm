#!/usr/bin/env bash
set -euo pipefail

# This script cleans the project folder by removing the root repository links so agents can be used for anything.
# It removes leftover assets, metadata, and git state that would tie the copy to the original repo.
# It also removes framework-development artifacts (including docs/) that aren't needed for a reusable snapshot.
rm -rf assets docs README.md tasks.html .DS_Store .git .gitattributes .github LICENSE tasks.json CONTRIBUTING.md CODE_OF_CONDUCT.md GUIDELINE.md

# Initialize a fresh repository after the cleanup so the folder can be reused independently.
git init
git add .AGENTS scripts .gitignore AGENTS.md
git commit -m "Initial commit"

rm -rf clean.sh
