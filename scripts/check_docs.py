#!/usr/bin/env python3
"""Validate the documentation source for the classes of mistake `npm run build` will not catch.

`next lint` never reads .md files, and `next build` only catches Markdoc *validation* errors — it is
perfectly happy with a link to a page that does not exist, a figure pointing at a missing image, or a
page that was never added to the sidebar. Those are the mistakes this repository has actually
accumulated, so they get their own check.

Checks:
  1. Every {% figure src %} resolves to a file under public/.
  2. Every internal link target resolves to a page, or to a redirect declared in next.config.js.
  3. Every {% callout type %} is exactly note or warning (any other value fails the build).
  4. Every {% quick-link icon %} is one of the six that Icon.jsx can resolve (an unknown icon is not
     validated by Markdoc — it crashes the page render at runtime).
  5. No page has an h3 before its first h2 (a hard build error).
  6. Page files and sidebar entries in Layout.jsx correspond exactly, in both directions.
  7. Every page has a title and a description in its frontmatter.

Usage:
    python scripts/check_docs.py

Exits non-zero if anything failed, so it is usable in CI.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PAGES_DIR = REPO_ROOT / "src" / "pages"
PUBLIC_DIR = REPO_ROOT / "public"
LAYOUT = REPO_ROOT / "src" / "components" / "Layout.jsx"
ICON_COMPONENT = REPO_ROOT / "src" / "components" / "Icon.jsx"
NEXT_CONFIG = REPO_ROOT / "next.config.js"

VALID_CALLOUT_TYPES = {"note", "warning"}

FIGURE_SRC = re.compile(r"\{%\s*figure[^%]*?src=\"([^\"]+)\"")
CALLOUT_TYPE = re.compile(r"\{%\s*callout[^%]*?type=\"([^\"]+)\"")
QUICK_LINK_ICON = re.compile(r"\{%\s*quick-link[^%]*?icon=\"([^\"]+)\"")
TAG_LINK_HREF = re.compile(r"\{%\s*link[^%]*?href=\"([^\"]+)\"")
MD_LINK = re.compile(r"\[[^\]]*\]\((/[^)\s]*)\)")
NAV_HREF = re.compile(r"href:\s*'([^']+)'")
ICON_KEY = re.compile(r"^\s*([a-z][a-zA-Z]*):\s", re.MULTILINE)
REDIRECT_SOURCE = re.compile(r"source:\s*'([^']+)'")
HEADING = re.compile(r"^(#{2,6})\s", re.MULTILINE)
HEADING_TEXT = re.compile(r"^#{2,6}\s+(.+?)\s*$", re.MULTILINE)
FENCE_BLOCK = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
INLINE_CODE = re.compile(r"`+[^`\n]*`+")


def without_code(text: str) -> str:
    """Strip fenced blocks and inline code before looking for tags and links.

    Pages that document this site's own authoring rules necessarily contain tag and link examples —
    including deliberately-wrong ones. Linting those would flag the documentation of a mistake as the
    mistake itself. Replace each block with blank lines so reported line context stays roughly right.
    """
    text = FENCE_BLOCK.sub(lambda match: "\n" * match.group().count("\n"), text)

    return INLINE_CODE.sub("", text)


def page_files() -> list[Path]:
    return sorted(PAGES_DIR.rglob("*.md"))


def route_for(path: Path) -> str:
    relative = path.relative_to(PAGES_DIR).with_suffix("")
    return "/" if relative.name == "index" and relative.parent == Path(".") else f"/{relative}"


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}

    end = text.find("\n---", 3)
    if end == -1:
        return {}

    result = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()

    return result


def slugify(heading: str) -> str:
    """Approximate @sindresorhus/slugify, which _app.jsx uses to generate heading ids."""
    text = re.sub(r"`([^`]*)`", r"\1", heading)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[^\w\s-]", "", text.lower())

    return re.sub(r"[\s_]+", "-", text).strip("-")


def anchors_of(text: str) -> set[str]:
    """Every heading id a page exposes, with the -1, -2 … suffixes duplicates receive."""
    seen: dict[str, int] = {}
    anchors = set()

    for heading in HEADING_TEXT.findall(text):
        slug = slugify(heading)
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        anchors.add(slug if count == 0 else f"{slug}-{count}")

    return anchors


def valid_icons() -> set[str]:
    """The icon names Icon.jsx can resolve, read out of its lookup object."""
    text = ICON_COMPONENT.read_text()
    start = text.find("const icons = {")
    if start == -1:
        return set()

    end = text.find("}", start)

    return set(ICON_KEY.findall(text[start:end]))


def main() -> int:
    problems: list[str] = []

    pages = page_files()
    routes = {route_for(path) for path in pages}
    icons = valid_icons()
    redirects = set(REDIRECT_SOURCE.findall(NEXT_CONFIG.read_text()))
    nav_hrefs = NAV_HREF.findall(LAYOUT.read_text())
    anchors_by_route = {
        route_for(path): anchors_of(without_code(path.read_text())) for path in pages
    }

    # 6. Sidebar and page files must correspond, in both directions.
    for href in nav_hrefs:
        if href not in routes:
            problems.append(f"{LAYOUT.name}: sidebar links {href}, but no page file produces it")

    for route in sorted(routes):
        if route not in nav_hrefs:
            problems.append(
                f"{route}: page exists but is missing from the sidebar in {LAYOUT.name} — "
                "it will render with no eyebrow, no highlight and no prev/next"
            )

    duplicates = {href for href in nav_hrefs if nav_hrefs.count(href) > 1}
    for href in sorted(duplicates):
        problems.append(f"{LAYOUT.name}: {href} appears more than once in the sidebar")

    for path in pages:
        raw = path.read_text()
        text = without_code(raw)
        label = path.relative_to(REPO_ROOT)

        # 7. Frontmatter.
        meta = frontmatter(raw)
        for key in ("title", "description"):
            if not meta.get(key):
                problems.append(f"{label}: frontmatter is missing {key}")

        # 1. Figures.
        for src in FIGURE_SRC.findall(text):
            if src.startswith(("http://", "https://")):
                continue
            if not (PUBLIC_DIR / src.lstrip("/")).is_file():
                problems.append(f"{label}: figure src {src} does not exist under public/")

        # 3. Callout types.
        for callout_type in CALLOUT_TYPE.findall(text):
            if callout_type not in VALID_CALLOUT_TYPES:
                problems.append(
                    f"{label}: callout type \"{callout_type}\" is invalid — "
                    f"must be one of {', '.join(sorted(VALID_CALLOUT_TYPES))}"
                )

        # 4. Quick-link icons.
        for icon in QUICK_LINK_ICON.findall(text):
            if icons and icon not in icons:
                problems.append(
                    f"{label}: quick-link icon \"{icon}\" is not in Icon.jsx — "
                    f"the page will crash. Valid: {', '.join(sorted(icons))}"
                )

        # 2. Internal links.
        for href in TAG_LINK_HREF.findall(text) + MD_LINK.findall(text):
            if not href.startswith("/"):
                problems.append(
                    f"{label}: internal link \"{href}\" is relative — "
                    "it resolves against the current directory. Use an absolute /docs/… path"
                )
                continue

            target, _, anchor = href.partition("#")
            target = target.rstrip("/") or "/"

            if target not in routes and target not in redirects:
                problems.append(f"{label}: link {href} points at a page that does not exist")
                continue

            # Anchors are only checkable against a real page; a redirect target's anchor is the
            # destination page's problem, not this link's.
            if anchor and target in anchors_by_route:
                if anchor not in anchors_by_route[target]:
                    problems.append(
                        f"{label}: link {href} points at an anchor that does not exist on {target} "
                        f"(available: {', '.join(sorted(anchors_by_route[target])) or 'none'})"
                    )

        # 5. h3 before the first h2.
        headings = HEADING.findall(text)
        if headings and len(headings[0]) > 2:
            problems.append(
                f"{label}: an h{len(headings[0])} appears before any h2 — this is a build error"
            )

    print(f"checked {len(pages)} page(s), {len(nav_hrefs)} sidebar entr(ies)")

    if problems:
        print(f"\n{len(problems)} problem(s):\n", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 1

    print("no problems found")

    return 0


if __name__ == "__main__":
    sys.exit(main())
