#!/usr/bin/env python3
"""
Append image references to each article .md file based on the images present
in docs/images/. Idempotent — safe to re-run after a sync wipes/overwrites
the markdown.

Image naming convention (set by process_images.py):
    docs/images/<article_slug>.jpg             # one image for this article
    docs/images/<article_slug>_1.jpg ... _N.jpg # multiple images for this article

For each group of images that share a base article_slug, the corresponding
docs/<article_slug>.md is updated to include `![Image](images/<file>)` lines,
inserted right after the first heading.
"""
from pathlib import Path
import re

HERE = Path(__file__).parent
DOCS = HERE / "docs"
IMG_DIR = DOCS / "images"

if not IMG_DIR.exists():
    print(f"No image dir at {IMG_DIR}, nothing to do.")
    raise SystemExit(0)

def resolve_article(image_name: str) -> str | None:
    """Map an image filename to the article slug whose .md exists in docs/.

    Tries the full stem first (handles article slugs that end in a digit,
    e.g. multiple_endocrine_neoplasia_type_1.md), then falls back to stripping
    a trailing _N suffix (used when multiple images share one article).
    """
    stem = image_name[:-4] if image_name.endswith(".jpg") else image_name
    if (DOCS / f"{stem}.md").exists():
        return stem
    stripped = re.sub(r"_\d+$", "", stem)
    if stripped != stem and (DOCS / f"{stripped}.md").exists():
        return stripped
    return None

per_article: dict[str, list[str]] = {}
unresolved: list[str] = []
for img in sorted(IMG_DIR.glob("*.jpg")):
    art = resolve_article(img.name)
    if art is None:
        unresolved.append(img.name)
        continue
    per_article.setdefault(art, []).append(img.name)

edits = 0
for slug, images in per_article.items():
    md = DOCS / f"{slug}.md"
    text = md.read_text(encoding="utf-8")
    new_lines = []
    for filename in images:
        # already referenced anywhere in the file? skip
        if f"images/{filename}" in text:
            continue
        new_lines.append(f"![Image](images/{filename})")
    if not new_lines:
        continue
    lines = text.splitlines()
    insert_at = 0
    for i, line in enumerate(lines):
        if re.match(r"^#{1,6}\s+", line):
            insert_at = i + 1
            break
    block = ["", *new_lines, ""]
    lines[insert_at:insert_at] = block
    md.write_text("\n".join(lines) + ("\n" if not text.endswith("\n") else ""), encoding="utf-8")
    edits += 1

print(f"Updated {edits} markdown file(s).")
if unresolved:
    print(f"Warning: {len(unresolved)} image(s) couldn't be matched to any article:")
    for n in unresolved[:10]:
        print(f"  - {n}")
    if len(unresolved) > 10:
        print(f"  ... and {len(unresolved) - 10} more")
