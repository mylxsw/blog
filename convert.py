#!/usr/bin/env python3
"""Convert md/mdx content under pages/ into Markdown with YAML front matter."""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

PAGES_DIR = Path(__file__).parent / "pages"
OUTPUT_DIR = Path(__file__).parent / "converted"

META_DATE_RE = re.compile(r"date=\{new Date\('([^']+)'\)\}")
META_TAGS_RE = re.compile(r"tags=\{\[([^\]]*)\]\}")
AI_NOTE_DATE_RE = re.compile(r"本文由\s*AI\s*创建于\s*(\d{4}-\d{2}-\d{2})")
FILENAME_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
IMPORT_LINE_RE = re.compile(r"^import .*$", re.MULTILINE)
META_COMPONENT_RE = re.compile('<Meta[^>]*>\\s*', re.IGNORECASE)
IMAGE_COMPONENT_RE = re.compile(
    r"""<Image\s+[^>]*src=(?:"([^"]+)"|'([^']+)'|\{`([^`]+)`\})[^>]*/?>""",
    re.IGNORECASE,
)


@dataclass
class ConversionMetadata:
    title: str
    date: str
    tags: List[str]


class MetaResolver:
    def __init__(self, pages_dir: Path) -> None:
        self.pages_dir = pages_dir.resolve()
        self._cache: Dict[Path, Dict[str, str]] = {}

    def _load_meta_for_dir(self, directory: Path) -> Dict[str, str]:
        directory = directory.resolve()
        if directory in self._cache:
            return self._cache[directory]

        mapping: Dict[str, str] = {}
        meta_path = directory / "_meta.json"
        if meta_path.exists():
            try:
                data = json.loads(meta_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Failed to parse {meta_path}: {exc}") from exc

            for key, value in data.items():
                if isinstance(value, str):
                    mapping[key] = value
                elif isinstance(value, dict):
                    title = value.get("title")
                    if isinstance(title, str):
                        mapping[key] = title
        self._cache[directory] = mapping
        return mapping

    def lookup_title(self, file_path: Path) -> Optional[str]:
        slug = file_path.stem
        directory = file_path.parent.resolve()

        current = directory
        while True:
            mapping = self._load_meta_for_dir(current)
            if slug in mapping:
                return mapping[slug]
            if current == self.pages_dir:
                break
            if current == current.parent:
                break
            current = current.parent
        return None


def parse_tags_from_meta(content: str) -> List[str]:
    match = META_TAGS_RE.search(content)
    if not match:
        return []
    raw = match.group(1)
    if not raw.strip():
        return []
    tags: List[str] = []
    for part in raw.split(","):
        cleaned = part.strip().strip("\"").strip("'")
        cleaned = cleaned.replace("\\\"", "\"")
        if cleaned:
            tags.append(cleaned)
    return tags


def parse_date(content: str, file_path: Path) -> str:
    match = META_DATE_RE.search(content)
    if match:
        return match.group(1)

    match = AI_NOTE_DATE_RE.search(content)
    if match:
        return match.group(1)

    match = FILENAME_DATE_RE.search(file_path.stem)
    if match:
        return match.group(1)

    return "1970-01-01"


def extract_title(content: str) -> Optional[str]:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return None


def clean_content(content: str) -> str:
    # Remove import statements
    content = IMPORT_LINE_RE.sub("", content)
    # Remove Meta component invocations
    content = META_COMPONENT_RE.sub("", content)

    # Convert Image components to Markdown syntax
    def _replace_image(match: re.Match) -> str:
        for group in match.groups():
            if group:
                return f"![]({group})"
        return ""

    content = IMAGE_COMPONENT_RE.sub(_replace_image, content)

    # Collapse multiple blank lines that may have been introduced
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content.strip() + "\n"


def quote_yaml_string(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace("\"", "\\\"")
    return f'"{escaped}"'


def format_tags(tags: List[str]) -> str:
    if not tags:
        return "[]"
    formatted = ", ".join(quote_yaml_string(tag) for tag in tags)
    return f"[{formatted}]"


def build_metadata(file_path: Path, content: str, resolver: MetaResolver) -> ConversionMetadata:
    title = resolver.lookup_title(file_path)
    if not title:
        heading_title = extract_title(content)
        title = heading_title or file_path.stem
    date = parse_date(content, file_path)
    tags = parse_tags_from_meta(content)
    return ConversionMetadata(title=title, date=date, tags=tags)


def convert_file(file_path: Path, resolver: MetaResolver) -> None:
    relative = file_path.relative_to(PAGES_DIR)
    output_path = OUTPUT_DIR / relative
    output_path = output_path.with_suffix(".md")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    content = file_path.read_text(encoding="utf-8")
    metadata = build_metadata(file_path, content, resolver)
    cleaned = clean_content(content)

    front_matter = "\n".join(
        [
            "---",
            f"title: {quote_yaml_string(metadata.title)}",
            f"date: {metadata.date}",
            f"tags: {format_tags(metadata.tags)}",
            "---",
            "",
        ]
    )

    output_path.write_text(front_matter + cleaned, encoding="utf-8")
    print(f"Converted {relative} -> {output_path.relative_to(OUTPUT_DIR)}")


def main() -> None:
    if not PAGES_DIR.exists():
        raise FileNotFoundError(f"Pages directory not found: {PAGES_DIR}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    resolver = MetaResolver(PAGES_DIR)

    files = sorted(
        path
        for path in PAGES_DIR.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".mdx"}
    )

    if not files:
        print("No Markdown or MDX files found under pages/.")
        return

    for file_path in files:
        convert_file(file_path, resolver)


if __name__ == "__main__":
    main()
