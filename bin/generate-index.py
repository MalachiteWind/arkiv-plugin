#!/usr/bin/env python3
"""Generate INDEX.md for arkiv (the .arkiv/ knowledge base).

INDEX.md is a runtime dispatcher. It is regenerated on demand from each
document's YAML frontmatter. Never hand-edit it.

Usage:
    generate-index.py [<path-to-.arkiv>]     # default: ./.arkiv

Standard library only (no third-party dependencies).

The frontmatter parser accepts a narrow, single-line subset:
  - "key: value" scalars, quoted or bare (a colon inside the value is kept)
  - inline lists in the form "key: [a, b, c]"
It rejects block or folded scalars ("|", ">") and malformed or absent
frontmatter. Every rejection prints a filename-specific warning to stderr and
is non-fatal: the document still appears in the index with a visible
"WARNING missing" marker in the affected cell, so the defect is easy to find.
"""

import sys
from datetime import date, datetime
from pathlib import Path

MISSING = "\u26a0 missing"   # visible marker for a missing required field
ABSENT = "\u2014"            # em dash: a genuinely optional field with no value
BLOCK_INDICATORS = {"|", ">", "|-", "|+", ">-", ">+", "|8", ">8"}


def warn(msg):
    print("generate-index: warning: " + msg, file=sys.stderr)


def parse_frontmatter(text, relpath):
    """Return (fields_dict, ok). ok is False when frontmatter is missing or malformed."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        warn(relpath + ": no YAML frontmatter block (expected a leading '---')")
        return {}, False
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        warn(relpath + ": frontmatter block is not closed with '---'")
        return {}, False

    fields = {}
    for raw in lines[1:end]:
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ": " not in line and not line.rstrip().endswith(":"):
            # continuation of a block scalar or otherwise unparseable line
            continue
        if ": " in line:
            key, value = line.split(": ", 1)
        else:
            key, value = line[:-1], ""
        key = key.strip()
        value = value.strip()
        if value in BLOCK_INDICATORS:
            warn(relpath + ": block/folded scalar for '" + key +
                 "' is not supported; use a single-line value")
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            items = [p.strip().strip("'\"") for p in inner.split(",")] if inner else []
            fields[key] = [p for p in items if p]
        else:
            fields[key] = value
    return fields, True


def date_or_min(value):
    if isinstance(value, str):
        try:
            return datetime.strptime(value.strip(), "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


def cell(value, required):
    """Render one table cell. Escape pipes and newlines. Flag missing required fields."""
    if value is None or value == "" or value == []:
        return MISSING if required else ABSENT
    if isinstance(value, list):
        value = ", ".join(value)
    text = str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")
    return text.strip() or (MISSING if required else ABSENT)


class Doc:
    def __init__(self, relpath, fields, ok):
        self.relpath = relpath
        self.fields = fields
        self.ok = ok

    def get(self, key):
        return self.fields.get(key)

    def flag_missing(self, required_keys):
        for k in required_keys:
            v = self.fields.get(k)
            if v is None or v == "" or v == []:
                warn(self.relpath + ": required field '" + k + "' is missing or empty")

    @property
    def sort_updated(self):
        return date_or_min(self.get("updated"))


def collect(arkiv_dir):
    docs = []
    for path in sorted(arkiv_dir.rglob("*.md")):
        relpath = path.relative_to(arkiv_dir).as_posix()
        if relpath == "INDEX.md":          # the only self-reference exclusion
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            warn(relpath + ": cannot read (" + str(exc) + ")")
            docs.append(Doc(relpath, {}, False))
            continue
        fields, ok = parse_frontmatter(text, relpath)
        docs.append(Doc(relpath, fields, ok))
    return docs


def category_of(relpath):
    parts = relpath.split("/")
    if len(parts) == 1:
        return "top"
    return parts[0]


def sort_group(docs):
    docs.sort(key=lambda d: d.relpath)                                   # path asc
    docs.sort(key=lambda d: d.sort_updated or date.min, reverse=True)    # updated desc, stable
    return docs


def render_table(docs, with_status):
    header = "| Title | Path | Updated |"
    sep = "|---|---|---|"
    if with_status:
        header += " Status |"
        sep += "---|"
    header += " Summary |"
    sep += "---|"
    rows = [header, sep]
    for d in docs:
        title = cell(d.get("title"), required=True)
        path = "`" + d.relpath + "`"
        updated = cell(d.get("updated"), required=True)
        summary = cell(d.get("summary"), required=True)
        line = "| " + title + " | " + path + " | " + updated + " |"
        if with_status:
            line += " " + cell(d.get("status"), required=True) + " |"
        line += " " + summary + " |"
        rows.append(line)
    return "\n".join(rows)


def main(argv):
    target = argv[1] if len(argv) > 1 else "./.arkiv"
    arkiv_dir = Path(target)
    if not arkiv_dir.is_dir():
        print("generate-index: error: arkiv directory not found: " + str(arkiv_dir),
              file=sys.stderr)
        return 2

    docs = collect(arkiv_dir)

    groups = {"top": [], "research": [], "dev": [], "handoff": []}
    extra = {}
    for d in docs:
        cat = category_of(d.relpath)
        if cat in groups:
            groups[cat].append(d)
        else:
            extra.setdefault(cat, []).append(d)

    # flag missing required fields per category (surfaces the defect on stderr too)
    for d in groups["top"]:
        d.flag_missing(["title", "summary", "updated"])
    for d in groups["dev"]:
        d.flag_missing(["title", "summary", "updated", "verified"])
    for d in groups["research"]:
        d.flag_missing(["title", "summary", "updated", "status"])
    for d in groups["handoff"]:
        d.flag_missing(["title", "summary", "updated"])

    generated = datetime.now().isoformat(timespec="seconds")
    out = []
    out.append("<!-- GENERATED by bin/generate-index.py - do not hand-edit. -->")
    out.append("<!-- Source of truth: each document's YAML frontmatter. Regenerate on demand. -->")
    out.append("")
    out.append("# INDEX")
    out.append("")
    out.append("Generated: " + generated)
    out.append("")

    sections = [
        ("Top-level", groups["top"], False),
        ("research/", groups["research"], True),
        ("dev/", groups["dev"], False),
        ("handoff/ (active)", groups["handoff"], False),
    ]
    for name in sorted(extra):
        sections.append((name + "/", extra[name], False))

    for title, group, with_status in sections:
        out.append("## " + title)
        out.append("")
        if group:
            out.append(render_table(sort_group(group), with_status))
        else:
            out.append("_none_")
        out.append("")

    index_path = arkiv_dir / "INDEX.md"
    index_path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print("generate-index: wrote " + index_path.as_posix() +
          " (" + str(len(docs)) + " documents)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
