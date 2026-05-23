#!/bin/bash
# Sync .md files from the source terms folder into docs/, preserving anything
# that exists only in docs/ (stub articles, etc.). After syncing, re-apply
# anki image references and regenerate the numbered nav.
#
# Safe to re-run. Does NOT delete files that exist in docs/ but not in source.

set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$(cd "$HERE/.." && pwd)/outputs/terms"
DST="$HERE/docs"

if [ ! -d "$SRC" ]; then
  echo "Source not found: $SRC" >&2
  exit 1
fi

# Copy/update source files into docs/, overwriting if they exist. Files in
# docs/ that don't exist in source are LEFT ALONE (this preserves the stub
# articles we create for orphan anki images).
COUNT=0
for f in "$SRC"/*.md; do
  cp "$f" "$DST/"
  COUNT=$((COUNT + 1))
done
echo "Synced $COUNT files from $SRC -> $DST"

# Re-append anki image references (idempotent: only adds refs that aren't
# already present in each .md).
python3 "$HERE/apply_image_refs.py"

# Regenerate the numbered nav in mkdocs.yml.
python3 "$HERE/build_nav.py"
