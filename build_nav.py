#!/usr/bin/env python3
"""Regenerate stub pages + numbered nav in mkdocs.yml.

Reads ../terms-completed.txt and ../terms-to-do.txt as the source of truth for
the full term universe. For any term that doesn't already have a .md file in
docs/, writes a placeholder stub. Then rewrites the nav: section of mkdocs.yml
with all entries alphabetically ordered and numbered, with a star on stubs.
"""
from pathlib import Path
import re

HERE = Path(__file__).parent
DOCS = HERE / "docs"
MKDOCS_YML = HERE / "mkdocs.yml"
COMPLETED_TXT = HERE.parent / "terms-completed.txt"
TODO_TXT = HERE.parent / "terms-to-do.txt"
STUB_MARKER = "This term has not been written yet."
STAR = " ⭐"

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")

def titleize(slug: str) -> str:
    return " ".join(w.capitalize() for w in slug.split("_"))

def read_terms(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {slugify(l) for l in path.read_text().splitlines() if l.strip()}

def is_stub(path: Path) -> bool:
    try:
        return STUB_MARKER in path.read_text(encoding="utf-8")
    except Exception:
        return False

def ensure_stubs() -> int:
    expected = read_terms(COMPLETED_TXT) | read_terms(TODO_TXT)
    existing = {p.stem for p in DOCS.glob("*.md") if p.name != "index.md"}
    missing = sorted(expected - existing)
    for slug in missing:
        title = titleize(slug)
        (DOCS / f"{slug}.md").write_text(
            f"## {title}\n\n_{STUB_MARKER}_\n", encoding="utf-8"
        )
    return len(missing)

def build_nav_lines() -> list[str]:
    md_files = sorted(p for p in DOCS.glob("*.md") if p.name != "index.md")
    lines = ["nav:", "  - Home: index.md"]
    for i, p in enumerate(md_files, start=1):
        title = f"{i}. {titleize(p.stem)}"
        if is_stub(p):
            title += STAR
        lines.append(f'  - "{title}": {p.name}')
    return lines

def main():
    created = ensure_stubs()
    text = MKDOCS_YML.read_text(encoding="utf-8")
    nav_block = "\n".join(build_nav_lines()) + "\n"
    pattern = re.compile(r"^nav:.*\Z", re.MULTILINE | re.DOTALL)
    if pattern.search(text):
        new_text = pattern.sub(nav_block.rstrip() + "\n", text)
    else:
        new_text = text.rstrip() + "\n\n" + nav_block
    MKDOCS_YML.write_text(new_text, encoding="utf-8")
    total = len([p for p in DOCS.glob("*.md") if p.name != "index.md"])
    stubs = sum(1 for p in DOCS.glob("*.md") if p.name != "index.md" and is_stub(p))
    print(f"Created {created} new stub(s); nav has {total} entries ({stubs} stubs).")

if __name__ == "__main__":
    main()
