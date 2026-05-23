#!/usr/bin/env python3
"""Regenerate stub pages + numbered nav in mkdocs.yml.

Steps:
1. From terms-completed.txt + terms-to-do.txt, create a stub .md for any
   missing slug so it shows up in the nav.
2. For each term .md, promote its first `## Heading` to `# Heading` so MkDocs
   treats it as the page's own h1 (instead of auto-injecting one from the nav
   title, which would result in a duplicate title at the top of the page).
3. Rewrite mkdocs.yml's nav: section with alphabetized, numbered entries.
   The displayed title uses the file's actual heading text (preserving casing
   like "AIDS"), with a star appended on stubs.
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

# Some terms in the txt files contain unicode (é, ñ, ü) that slugifies away
# letters, producing different slugs than the actual file names (which were
# generated separately and preserved more letters). Map txt-slug -> file-slug
# so we don't create duplicate stub files for terms that already exist.
SLUG_ALIASES = {
    "guillain_barr_syndrome": "guillain_barr_e_syndrome",
    "legg_calv_perthes_disease": "legg_calv_e_perthes_disease",
    "m_llerian_agenesis": "m_ullerian_agenesis",
    "m_ni_re_disease": "m_eni_ere_disease",
}

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
    expected = {SLUG_ALIASES.get(s, s) for s in expected}
    existing = {p.stem for p in DOCS.glob("*.md") if p.name != "index.md"}
    missing = sorted(expected - existing)
    for slug in missing:
        title = titleize(slug)
        (DOCS / f"{slug}.md").write_text(
            f"# {title}\n\n_{STUB_MARKER}_\n", encoding="utf-8"
        )
    return len(missing)

def promote_first_h2_to_h1(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if re.search(r"^# ", text, re.MULTILINE):
        return  # already has an h1
    new_text, n = re.subn(r"^## ", "# ", text, count=1, flags=re.MULTILINE)
    if n:
        path.write_text(new_text, encoding="utf-8")

def first_heading_text(path: Path) -> str | None:
    """Return the text of the first markdown heading (any level) in the file."""
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    return None

def build_nav_lines() -> list[str]:
    md_files = sorted(p for p in DOCS.glob("*.md") if p.name != "index.md")
    lines = ["nav:", "  - Home: index.md"]
    for i, p in enumerate(md_files, start=1):
        heading = first_heading_text(p) or titleize(p.stem)
        title = f"{i}. {heading}"
        if is_stub(p):
            title += STAR
        # Escape any embedded double quotes
        safe = title.replace('"', '\\"')
        lines.append(f'  - "{safe}": {p.name}')
    return lines

def main():
    created = ensure_stubs()
    # Promote first ## to # in every term file so the page has its own h1.
    for p in DOCS.glob("*.md"):
        if p.name == "index.md":
            continue
        promote_first_h2_to_h1(p)
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
