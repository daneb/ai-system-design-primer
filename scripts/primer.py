#!/usr/bin/env python3
"""Primer maintenance tool. Standard library only.

  python3 scripts/primer.py check          validate front matter; fail on overdue reviews
  python3 scripts/primer.py status         print progress by phase
  python3 scripts/primer.py readme         regenerate the TOC and progress blocks in README.md
  python3 scripts/primer.py flashcards     export Q/A blocks to build/flashcards.tsv (Anki import)
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DEEP = DOCS / "deep-dives"
README = ROOT / "README.md"

MATURITY = {"stable", "mixed", "frontier", "speculative"}
STATUS = {"planned", "draft", "review", "published"}
HUB_SECTIONS = {"3.4", "3.9", "3.17"}


MAX_TABLES = 1          # primer pages: at most one table (STYLE.md)
MAX_EXTERNAL_LINKS = 8  # primer pages, excluding the Sources list


def word_budget(sid):
    part = sid.split(".")[0]
    if sid in HUB_SECTIONS:
        return 1200
    return {"0": 1400, "1": 1400, "2": 800, "3": 800, "4": 2500}.get(part)


def reading_body(body):
    """The part of a primer page a learner reads: up to Flashcards or Sources, code fences removed."""
    body = re.split(r"^## (?:Flashcards|Sources and further reading)\s*$", body, flags=re.M)[0]
    return re.sub(r"```.*?```", "", body, flags=re.S)


def body_words(body):
    """Words counted against the budget: the reading body minus the Key terms box (reference material)."""
    text = re.sub(r"^## Key terms\s*$.*?(?=^## )", "", reading_body(body), flags=re.S | re.M)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)|<!--.*?-->", "", text, flags=re.S)  # diagram alt text is not reading
    return len(re.findall(r"\S+", text))


GLOSSARY = DOCS / "5-appendix" / "5.6-glossary.md"
# Acronyms readers are assumed to know; everything else must be in the glossary.
COMMON_ACRONYMS = {"AI", "API", "APIs", "ID", "IDs", "URL", "URLs", "HTTP", "HTTPS", "JSON", "PDF", "CPU",
                   "CPUs", "GPU", "GPUs", "SQL", "UI", "CI", "US", "EU", "UK", "OK", "SDK", "SDKs", "CSV",
                   "KB", "MB", "GB", "TB", "PR", "PRs", "FAQ", "IT", "HR", "CEO", "README", "TL", "DR",
                   "AWS", "GCP", "VM", "VMs", "OS", "IDE", "CLI", "RAM", "Q", "A", "HTML", "CSS", "XML", "SMS", "BCC", "CC"}
KEY_TERMS_PARTS = ("0", "1", "2", "3")     # primer pages that need a Key terms box and an example
LONG_SENTENCE = 30


def glossary_terms():
    """Terms (lower-case) and acronyms defined in the glossary's first column."""
    terms, acronyms, dupes = set(), set(), []
    if not GLOSSARY.exists():
        return terms, acronyms, dupes
    for line in GLOSSARY.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| ([^|]+?) \| [^|]+ \| [^|]*\|\s*$", line)
        if not m or m.group(1) in ("Term", "Date") or m.group(1).startswith("-"):
            continue
        term = m.group(1).strip()
        if re.match(r"\d{4}-\d{2}-\d{2}", term):
            continue
        key = term.lower()
        if key in terms:
            dupes.append(term)
        terms.add(key)
        acronyms.update(re.findall(r"[A-Z][A-Z0-9]{1,6}", term))
    return terms, acronyms, dupes


def plain_text(body):
    """Reading body with links reduced to their text, inline code and HTML comments removed."""
    t = reading_body(body)
    t = re.sub(r"`[^`]*`", "", t)
    t = re.sub(r"\]\([^)]*\)", "]", t)
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = re.sub(r"\b[A-Z]{1,6}-\d+\b", "", t)          # identifiers such as TX-4471
    return t


def undefined_acronyms(body, known):
    found = set(re.findall(r"\b[A-Z][A-Z0-9]{1,6}s?\b", plain_text(body)))
    found = {a for a in found if not re.fullmatch(r"(LLM|ASI)\d\d|[IVX]+|[A-Z]\d+", a)}   # list IDs, numerals, model codes
    return sorted(a for a in found
                  if a not in COMMON_ACRONYMS and a not in known and a.rstrip("s") not in known)


def long_sentences(body):
    text = re.sub(r"^\s*\|.*$", "", plain_text(body), flags=re.M)     # skip tables
    out = []
    # list items and headings are separate units even without a full stop
    for unit in re.split(r"\n\s*\n|\n(?=\s*(?:[-*]|\d+\.)\s)|\n(?=#)", text):
        unit = re.sub(r"\s+", " ", unit).strip()
        out += [s for s in re.split(r"(?<=[.!?:;])\s+", unit) if len(s.split()) > LONG_SENTENCE]
    return out


def table_count(body):
    return len(re.findall(r"^\|[-: |]+\|\s*$", reading_body(body), flags=re.M))


def external_links(body):
    return len(re.findall(r"\]\(https?://", reading_body(body)))


REVIEW_MONTHS = {"stable": 12, "mixed": 6, "frontier": 3, "speculative": 3}
BADGE = {"stable": "S", "mixed": "S/F", "frontier": "F", "speculative": "?"}
PARTS = {
    "0": "Part 0: Orientation",
    "1": "Part 1: Method",
    "2": "Part 2: Trade-offs",
    "3": "Part 3: Components, in request order",
    "4": "Part 4: Solved designs",
    "5": "Part 5: Appendix",
}


def parse_front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    meta, key = {}, None
    for raw in m.group(1).splitlines():
        line = raw.split(" #", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.lstrip().startswith("- ") and key:
            if meta.get(key) is None:
                meta[key] = []
            if isinstance(meta[key], list):
                meta[key].append(line.strip()[2:].strip().strip('"'))
            continue
        k, _, v = line.partition(":")
        key = k.strip()
        v = v.strip().strip('"')
        meta[key] = v if v else None
    return meta, text[m.end():]


def id_key(sid):
    return tuple(int(p) for p in sid.split("."))


def load_deep_dives():
    out = []
    for path in sorted(DEEP.glob("*.md")) if DEEP.exists() else []:
        meta, body = parse_front_matter(path.read_text(encoding="utf-8"))
        out.append({"path": path, "meta": meta or {}, "body": body})
    return out


def deep_dive_for(sid):
    for d in load_deep_dives():
        if d["meta"].get("id") == sid:
            return d["path"]
    return None


def load_sections():
    """Primer pages only (deep dives are loaded separately)."""
    out = []
    for path in DOCS.rglob("*.md"):
        if DEEP in path.parents:
            continue
        meta, body = parse_front_matter(path.read_text(encoding="utf-8"))
        out.append({"path": path, "meta": meta or {}, "body": body})
    out.sort(key=lambda s: id_key(s["meta"].get("id") or "99"))
    return out


def parse_date(v):
    try:
        return dt.date.fromisoformat(v) if v else None
    except ValueError:
        return "invalid"


def cmd_check(args):
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    errors, warnings, seen = [], [], set()
    g_terms, g_acronyms, g_dupes = glossary_terms()
    for d in g_dupes:
        errors.append(f"{GLOSSARY.relative_to(ROOT)}: duplicate glossary term '{d}'")
    long_total = 0
    for s in load_sections():
        m, rel = s["meta"], s["path"].relative_to(ROOT)
        if not m:
            errors.append(f"{rel}: missing front matter")
            continue
        sid = m.get("id")
        if not sid or not re.fullmatch(r"\d+(\.\d+)?", sid):
            errors.append(f"{rel}: id missing or malformed")
            continue
        if sid in seen:
            errors.append(f"{rel}: duplicate id {sid}")
        seen.add(sid)
        if not s["path"].name.startswith(f"{sid}-"):
            errors.append(f"{rel}: file name should start with '{sid}-'")
        if m.get("maturity") not in MATURITY:
            errors.append(f"{rel}: maturity must be one of {sorted(MATURITY)}")
        if m.get("status") not in STATUS:
            errors.append(f"{rel}: status must be one of {sorted(STATUS)}")
        if not m.get("title"):
            errors.append(f"{rel}: title missing")
        if m.get("status") == "planned":
            continue
        for field in ("last_verified", "review_by", "owner"):
            if not m.get(field):
                errors.append(f"{rel}: {field} is required once status is not 'planned'")
        lv, rb = parse_date(m.get("last_verified")), parse_date(m.get("review_by"))
        if "invalid" in (lv, rb):
            errors.append(f"{rel}: dates must be YYYY-MM-DD")
            continue
        if lv and rb:
            limit = REVIEW_MONTHS.get(m.get("maturity"), 3)
            if (rb - lv).days > limit * 31:
                errors.append(f"{rel}: review_by is more than {limit} months after last_verified "
                              f"for maturity '{m.get('maturity')}'")
            if rb < today:
                (warnings if args.warn_only else errors).append(
                    f"{rel}: review overdue (review_by {rb}); re-verify sources and bump dates")
        budget = word_budget(sid)
        words = body_words(s["body"])
        if budget and words > budget:
            warnings.append(f"{rel}: {words} words, over the {budget}-word budget in STYLE.md")
        if sid.split(".")[0] in ("2", "3"):
            if table_count(s["body"]) > MAX_TABLES:
                warnings.append(f"{rel}: {table_count(s['body'])} tables; primer pages allow {MAX_TABLES}")
            if external_links(s["body"]) > MAX_EXTERNAL_LINKS:
                warnings.append(f"{rel}: {external_links(s['body'])} external links in the reading text; "
                                f"move them to Sources or the deep dive (limit {MAX_EXTERNAL_LINKS})")
            if not deep_dive_for(sid):
                warnings.append(f"{rel}: no deep dive in docs/deep-dives/ (ADR 0007)")
        if "## Flashcards" not in s["body"]:
            warnings.append(f"{rel}: no '## Flashcards' heading")
        if sid.split(".")[0] in KEY_TERMS_PARTS:
            if not re.search(r"^## Key terms\s*$", s["body"], re.M):
                warnings.append(f"{rel}: no '## Key terms' box (ROADMAP theme 1)")
            if not re.search(r"^#{2,3} (?:Worked e|E)xample\b", s["body"], re.M):
                warnings.append(f"{rel}: no '### Example' worked example (ROADMAP theme 1)")
        missing = undefined_acronyms(s["body"], g_acronyms) if sid.split(".")[0] != "5" else []
        if missing:
            warnings.append(f"{rel}: acronyms not in the glossary: {', '.join(missing)}")
        if sid.split(".")[0] in KEY_TERMS_PARTS:
            longs = long_sentences(s["body"])
            long_total += len(longs)
            for sentence in longs:
                warnings.append(f"{rel}: sentence over {LONG_SENTENCE} words: \"{sentence[:70]}...\"")
    primer_ids = {s["meta"].get("id") for s in load_sections()}
    for d in load_deep_dives():
        m, rel = d["meta"], d["path"].relative_to(ROOT)
        sid = m.get("id")
        if m.get("layer") != "deep-dive":
            errors.append(f"{rel}: deep dives need 'layer: deep-dive'")
        if sid not in primer_ids:
            errors.append(f"{rel}: no primer page with id {sid}")
        elif not d["path"].name.startswith(f"{sid}-"):
            errors.append(f"{rel}: file name should start with '{sid}-'")
        lv, rb = parse_date(m.get("last_verified")), parse_date(m.get("review_by"))
        if not lv or not rb or "invalid" in (lv, rb):
            errors.append(f"{rel}: last_verified and review_by must be YYYY-MM-DD")
        elif rb < today:
            (warnings if args.warn_only else errors).append(f"{rel}: review overdue (review_by {rb})")
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"{len(seen)} sections checked, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


def status_table():
    sections = load_sections()
    lines = ["| Phase | Sections | Planned | Draft | Review | Published |", "|---|---|---|---|---|---|"]
    for phase in sorted({int(s["meta"].get("phase") or 0) for s in sections}):
        group = [s for s in sections if int(s["meta"].get("phase") or 0) == phase]
        counts = {k: sum(1 for s in group if s["meta"].get("status") == k) for k in STATUS}
        lines.append(f"| {phase} | {len(group)} | {counts['planned']} | {counts['draft']} | "
                     f"{counts['review']} | {counts['published']} |")
    return "\n".join(lines)


def cmd_status(args):
    print(status_table())
    return 0


def toc():
    lines, current = [], None
    for s in load_sections():
        m = s["meta"]
        part = m["id"].split(".")[0]
        if part != current:
            current = part
            lines.append(f"\n**{PARTS.get(part, 'Part ' + part)}**\n")
        rel = s["path"].relative_to(ROOT).as_posix()
        mark = "" if m.get("status") in ("draft", "review", "published") else " _(planned)_"
        deep = deep_dive_for(m["id"])
        deep_link = f" · [deep dive]({deep.relative_to(ROOT).as_posix()})" if deep else ""
        lines.append(f"- [{m['id']} {m['title']}]({rel}) `{BADGE.get(m.get('maturity'), '?')}`{mark}{deep_link}")
    return "\n".join(lines).strip()


def replace_block(text, name, content):
    pattern = re.compile(rf"(<!-- {name}:start -->).*?(<!-- {name}:end -->)", re.S)
    if not pattern.search(text):
        raise SystemExit(f"README.md has no '{name}' markers")
    return pattern.sub(lambda m: m.group(1) + "\n" + content + "\n" + m.group(2), text)


CLOUD_COLS = ["Azure", "AWS", "Google Cloud", "OpenAI", "Anthropic", "Open source"]
CLOUD_NORM = {"Azure / Microsoft": "Azure", "Self-hosted / open source": "Open source"}
CLOUD_GROUPS = {
    "Cost, capacity and model access": ["2.1", "2.7", "3.1", "3.7", "3.13", "3.14"],
    "Retrieval and knowledge": ["2.3", "3.4", "3.5", "3.6"],
    "Agents, context and memory": ["2.5", "3.3", "3.9", "3.10", "3.11"],
    "Safety, security and quality": ["3.2", "3.12", "3.15", "3.16", "3.17"],
    "Serving and adaptation": ["2.6", "3.8", "3.18"],
}


def cloudmap():
    """Merge every deep dive's 'Cloud mapping' table into one set of tables for 5.2."""
    files = {p.name.split("-")[0]: p for p in DEEP.glob("*.md")}
    fix = lambda x: re.sub(r"\]\((\d[\d.]*-[^)]+\.md)\)", r"](../deep-dives/\1)", x)
    out = []
    for group, ids in CLOUD_GROUPS.items():
        out += [f"### {group}", "", "| Capability | " + " | ".join(CLOUD_COLS) + " |",
                "|" + "---|" * (len(CLOUD_COLS) + 1)]
        for sid in ids:
            path = files.get(sid)
            if not path:
                continue
            m = re.search(r"^## Cloud mapping\n(.*?)(?=^## |\Z)", path.read_text(encoding="utf-8"), re.S | re.M)
            if not m:
                continue
            rows = [l for l in m.group(1).splitlines() if l.startswith("|")]
            hdr = [CLOUD_NORM.get(h.strip(), h.strip()) for h in rows[0].strip("|").split("|")]
            for r in rows[2:]:
                cells = [c.strip() for c in r.strip("|").split("|")]
                if not cells[0]:
                    continue
                d = dict(zip(hdr[1:], cells[1:]))
                vals = [fix(d.get(c, "")) or "·" for c in CLOUD_COLS]
                out.append(f"| {fix(cells[0])} ([{sid}](../deep-dives/{path.name})) | " + " | ".join(vals) + " |")
        out.append("")
    return "\n".join(out).strip()


def akamap():
    """Collect each section's 'aka' names (other vendors' and researchers' names) for 5.3."""
    out = ["| Section | Also known as |", "|---|---|"]
    for s in load_sections():
        m = s["meta"]
        aka = m.get("aka")
        if not aka or m.get("status") == "planned":
            continue
        names = "<br>".join(aka) if isinstance(aka, list) else str(aka)
        rel = "../" + s["path"].relative_to(DOCS).as_posix()
        out.append(f"| [{m['id']} {m['title']}]({rel}) | {names} |")
    return "\n".join(out)


def refresh_appendix(check):
    """Regenerate the generated blocks in 5.2 and 5.3. Returns True if anything changed."""
    changed = False
    for name, func in [("cloudmap", cloudmap), ("akamap", akamap)]:
        for path in (DOCS / "5-appendix").glob("*.md"):
            text = path.read_text(encoding="utf-8")
            if f"<!-- {name}:start -->" not in text:
                continue
            new = replace_block(text, name, func())
            if new != text:
                changed = True
                if not check:
                    path.write_text(new, encoding="utf-8")
    return changed


def cmd_readme(args):
    text = README.read_text(encoding="utf-8")
    new = replace_block(replace_block(text, "toc", toc()), "status", status_table())
    appendix_changed = refresh_appendix(args.check)
    if args.check:
        if new != text or appendix_changed:
            print("README.md or generated appendix tables are out of date; run: python3 scripts/primer.py readme")
            return 1
        print("README.md is up to date")
        return 0
    README.write_text(new, encoding="utf-8")
    print("README.md updated")
    return 0


def cmd_flashcards(args):
    rows = []
    for s in load_sections():
        m = s["meta"]
        if m.get("status") == "planned":
            continue
        block = re.search(r"^## Flashcards\s*\n(.*?)(?=^## |\Z)", s["body"], re.S | re.M)
        if not block:
            continue
        for q, a in re.findall(r"^Q:\s*(.+?)\s*\nA:\s*(.+?)(?=\n\s*\n|\nQ:|\Z)", block.group(1), re.S | re.M):
            clean = lambda t: " ".join(t.split()).replace("\t", " ")
            tags = f"primer::{m['id'].replace('.', '_')} maturity::{m.get('maturity')}"
            rows.append(f"{clean(q)}\t{clean(a)}\t{tags}")
    out = ROOT / "build" / "flashcards.tsv"
    out.parent.mkdir(exist_ok=True)
    out.write_text("#separator:tab\n#html:false\n#tags column:3\n" + "\n".join(rows) + "\n", encoding="utf-8")
    print(f"{len(rows)} cards written to {out.relative_to(ROOT)}")
    return 0


def cmd_labs(args):
    """Run every lab script from its own folder; fail if any exits non-zero."""
    import subprocess
    failed = 0
    scripts = sorted((ROOT / "labs").glob("*/*.py"))
    for script in scripts:
        r = subprocess.run([sys.executable, script.name], cwd=script.parent, capture_output=True, text=True, timeout=600)
        status = "ok" if r.returncode == 0 else f"FAILED ({r.returncode})"
        print(f"{status:<12} {script.relative_to(ROOT)}")
        if r.returncode != 0:
            failed += 1
            print(r.stderr[-2000:])
    print(f"{len(scripts) - failed}/{len(scripts)} labs ran")
    charts = 0
    for script in scripts:
        if "line_chart(" not in script.read_text(encoding="utf-8"):
            continue
        charts += 1
        svg, readme = script.parent / "result.svg", script.parent / "README.md"
        if not svg.exists():
            failed += 1; print(f"FAILED       {svg.relative_to(ROOT)} not written (is matplotlib installed?)")
        elif "](result.svg)" not in readme.read_text(encoding="utf-8"):
            failed += 1; print(f"FAILED       {readme.relative_to(ROOT)} doesn't show result.svg")
    print(f"{charts} lab charts checked")
    return 1 if failed else 0


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("--warn-only", action="store_true", help="report overdue reviews as warnings")
    c.add_argument("--today", help="override today's date (YYYY-MM-DD), for testing")
    sub.add_parser("status")
    r = sub.add_parser("readme")
    r.add_argument("--check", action="store_true", help="exit 1 if README.md would change")
    sub.add_parser("flashcards")
    sub.add_parser("labs")
    args = p.parse_args()
    return {"check": cmd_check, "status": cmd_status, "readme": cmd_readme, "flashcards": cmd_flashcards, "labs": cmd_labs}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
