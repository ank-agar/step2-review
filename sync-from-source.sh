#!/bin/bash
# Re-copy .md files from the source terms folder into docs/.
# Run this whenever you regenerate content in chatgpt-content-review-2/outputs/terms.

set -euo pipefail

SRC="$(cd "$(dirname "$0")/.." && pwd)/outputs/terms"
DST="$(cd "$(dirname "$0")" && pwd)/docs"

if [ ! -d "$SRC" ]; then
  echo "Source not found: $SRC" >&2
  exit 1
fi

# Remove old term files (keep index.md)
find "$DST" -maxdepth 1 -type f -name "*.md" ! -name "index.md" -delete

cp "$SRC"/*.md "$DST"/
echo "Copied $(ls "$SRC"/*.md | wc -l | tr -d ' ') files from $SRC -> $DST"
