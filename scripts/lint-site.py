#!/usr/bin/env python3
"""Validate the dependency-free GitHub Pages source."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT


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
    pages: dict[Path, SiteParser] = {}
    for page in sorted(SITE.glob("*.html")):
        parser = SiteParser()
        parser.feed(page.read_text())
        parser.close()
        pages[page.resolve()] = parser

        prefix = f"{page.name}: "
        if parser.duplicate_ids:
            errors.append(f"{prefix}duplicate ids: {sorted(parser.duplicate_ids)}")
        if parser.html_lang != "en":
            errors.append(f"{prefix}must declare lang=en")
        if parser.h1_count != 1:
            errors.append(f"{prefix}must contain exactly one h1, found {parser.h1_count}")
        if not parser.title.strip():
            errors.append(f"{prefix}has no document title")
        if not parser.description:
            errors.append(f"{prefix}has no meta description")

    for page, parser in pages.items():
        for tag, reference in parser.references:
            parsed = urlparse(reference)
            if parsed.scheme or reference.startswith("//"):
                continue
            prefix = f"{page.name}: {tag} reference {reference!r}"
            if reference.startswith("/"):
                errors.append(f"{prefix} is root-relative and not preview-portable")
                continue

            target = page if not parsed.path else (page.parent / parsed.path).resolve()
            if not target.is_file():
                errors.append(f"{prefix} does not exist")
                continue
            if parsed.fragment and target.suffix == ".html":
                target_parser = pages.get(target)
                if not target_parser or parsed.fragment not in target_parser.ids:
                    errors.append(f"{prefix} has no matching id")

    css = (SITE / "styles.css").read_text()
    if css.count("{") != css.count("}"):
        errors.append("styles.css has unbalanced rule braces")

    if errors:
        for error in errors:
            print(f"site lint: {error}")
        return 1

    print(
        f"site lint: clean ({len(pages)} pages, "
        f"{sum(len(parser.references) for parser in pages.values())} links/assets)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
