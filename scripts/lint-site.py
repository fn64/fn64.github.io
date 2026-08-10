#!/usr/bin/env python3
"""Validate the dependency-free GitHub Pages source."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT
INDEX = SITE / "index.html"


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.references: list[tuple[str, str]] = []
        self.html_lang: str | None = None
        self.h1_count = 0
        self.title_depth = 0
        self.title = ""
        self.description: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicate_ids.add(element_id)
            self.ids.add(element_id)

        for attribute in ("href", "src"):
            reference = values.get(attribute)
            if reference:
                self.references.append((tag, reference))

        if tag == "html":
            self.html_lang = values.get("lang")
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "title":
            self.title_depth += 1
        elif tag == "meta" and values.get("name") == "description":
            self.description = values.get("content")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.title_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title += data


def main() -> int:
    errors: list[str] = []
    parser = SiteParser()
    parser.feed(INDEX.read_text())
    parser.close()

    if parser.duplicate_ids:
        errors.append(f"duplicate ids: {sorted(parser.duplicate_ids)}")
    if parser.html_lang != "en":
        errors.append("index.html must declare lang=en")
    if parser.h1_count != 1:
        errors.append(f"index.html must contain exactly one h1, found {parser.h1_count}")
    if not parser.title.strip():
        errors.append("index.html has no document title")
    if not parser.description:
        errors.append("index.html has no meta description")

    for tag, reference in parser.references:
        parsed = urlparse(reference)
        if parsed.scheme or reference.startswith("//"):
            continue
        if reference.startswith("/"):
            errors.append(
                f"{tag} reference {reference!r} is root-relative and will break under /fn64/"
            )
            continue
        if reference.startswith("#"):
            if reference[1:] not in parser.ids:
                errors.append(f"{tag} reference {reference!r} has no matching id")
            continue

        target = SITE / parsed.path
        if not target.is_file():
            errors.append(f"{tag} reference {reference!r} does not exist under site/")

    css = (SITE / "styles.css").read_text()
    if css.count("{") != css.count("}"):
        errors.append("styles.css has unbalanced rule braces")

    if errors:
        for error in errors:
            print(f"site lint: {error}")
        return 1

    print(
        f"site lint: clean ({len(parser.ids)} ids, "
        f"{len(parser.references)} links/assets)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
