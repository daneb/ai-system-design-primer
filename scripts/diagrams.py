#!/usr/bin/env python3
"""Diagram pipeline: Mermaid sources in images/src/*.mmd -> rendered SVGs in images/*.svg.

  python3 scripts/diagrams.py extract   # one-off: move ```mermaid blocks out of pages into images/src
  python3 scripts/diagrams.py render    # render every .mmd with the shared theme (needs Node: npx mmdc)
  python3 scripts/diagrams.py sync-alt  # copy each source's alt line into the pages that show it
  python3 scripts/diagrams.py check     # every image link has alt text, a source, and an up-to-date SVG

Each .mmd starts with '%% alt: <text>' (the image's alt text). The renderer prepends the shared
classDefs (STYLE.md, "Diagrams") to flowcharts, so sources can use 'class X model' etc. The SHA-256 of
each rendered source is kept in images/.hashes.json so CI can spot a stale SVG without running Node.
"""
import hashlib, json, pathlib, re, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMAGES, SRC = ROOT / "images", ROOT / "images" / "src"
CONFIG, HASHES = IMAGES / "mermaid-config.json", IMAGES / ".hashes.json"
CLASSDEFS = """
classDef model fill:#EEF2FF,stroke:#4F46E5,color:#1E1B4B
classDef tool fill:#ECFDF5,stroke:#059669,color:#064E3B
classDef data fill:#FFFBEB,stroke:#D97706,color:#78350F
classDef human fill:#F1F5F9,stroke:#475569,color:#0F172A
classDef untrusted fill:#FEF2F2,stroke:#DC2626,color:#7F1D1D,stroke-dasharray:4 3
classDef control fill:#F5F3FF,stroke:#7C3AED,color:#3B0764
""".strip()
IMG = re.compile(r"!\[([^\]]*)\]\(((?:\.\./)*images/([^)]+)\.svg)\)")


def pages():
    yield ROOT / "README.md"
    yield from sorted((ROOT / "docs").rglob("*.md"))


def labels(src):
    out = []
    for m in re.finditer(r'[\[\(\{]+"?([^\]\)\}"]+)"?[\]\)\}]+', src):
        t = re.sub(r"<br\s*/?>", " ", m.group(1)).strip()
        if t and t not in out:
            out.append(t)
    return out


def extract():
    for page in pages():
        text = page.read_text(encoding="utf-8")
        blocks = list(re.finditer(r"```mermaid\n(.*?)```\n", text, re.S))
        if not blocks:
            continue
        title = re.search(r"^# (.+)$", text, re.M)
        title = title.group(1) if title else "the primer"
        rel = pathlib.Path("../" * (len(page.relative_to(ROOT).parts) - 1))
        new, last = [], 0
        for i, b in enumerate(blocks):
            stem = page.stem if page.name != "README.md" else "readme"
            name = stem + (f"-{i + 1}" if len(blocks) > 1 else "")
            src = b.group(1)
            alt = f"Diagram for {title}: " + ", ".join(labels(src))
            alt = alt[:240].rsplit(",", 1)[0] if len(alt) > 240 else alt
            (SRC / f"{name}.mmd").write_text(f"%% alt: {alt}\n{src}", encoding="utf-8")
            img = (rel / "images" / f"{name}.svg").as_posix()
            new.append(text[last:b.start()])
            new.append(f"![{alt}]({img})\n<!-- source: images/src/{name}.mmd; render with scripts/diagrams.py -->\n")
            last = b.end()
        new.append(text[last:])
        page.write_text("".join(new), encoding="utf-8")
        print(f"{page.relative_to(ROOT)}: {len(blocks)} diagram(s)")


def with_classdefs(src):
    body = "\n".join(l for l in src.splitlines() if not l.startswith("%% alt:"))
    lines = body.splitlines()
    if lines and re.match(r"\s*(flowchart|graph)\b", lines[0]):
        return "\n".join([lines[0], CLASSDEFS] + lines[1:]) + "\n"
    return body + "\n"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def render():
    mmdc = shutil.which("mmdc")
    cmd = [mmdc] if mmdc else ["npx", "-y", "@mermaid-js/mermaid-cli"]
    hashes = json.loads(HASHES.read_text()) if HASHES.exists() else {}
    tmp = IMAGES / ".tmp.mmd"
    for src in sorted(SRC.glob("*.mmd")):
        tmp.write_text(with_classdefs(src.read_text(encoding="utf-8")), encoding="utf-8")
        out = IMAGES / f"{src.stem}.svg"
        r = subprocess.run(cmd + ["-i", str(tmp), "-o", str(out), "-c", str(CONFIG), "-b", "white"],
                           capture_output=True, text=True)
        if r.returncode:
            print(f"FAILED {src.name}\n{r.stderr[-800:]}")
            continue
        hashes[src.name] = digest(src)
        print(f"rendered {out.relative_to(ROOT)}")
    tmp.unlink(missing_ok=True)
    HASHES.write_text(json.dumps(hashes, indent=1, sort_keys=True) + "\n")


def sync_alt():
    """Copy each source's '%% alt:' line into the image links that use it."""
    alts = {}
    for src in SRC.glob("*.mmd"):
        first = src.read_text(encoding="utf-8").splitlines()[0]
        if first.startswith("%% alt:"):
            alts[src.stem] = first[len("%% alt:"):].strip().replace("]", ")").replace("[", "(")
    for page in pages():
        text = page.read_text(encoding="utf-8")
        new = IMG.sub(lambda m: f"![{alts.get(m.group(3), m.group(1))}]({m.group(2)})", text)
        if new != text:
            page.write_text(new, encoding="utf-8")
            print(f"alt text updated in {page.relative_to(ROOT)}")


def check():
    problems = []
    hashes = json.loads(HASHES.read_text()) if HASHES.exists() else {}
    for page in pages():
        text = page.read_text(encoding="utf-8")
        if "```mermaid" in text:
            problems.append(f"{page.relative_to(ROOT)}: inline mermaid; move it to images/src (diagrams.py extract)")
        for alt, link, name in IMG.findall(text):
            if len(alt.strip()) < 15:
                problems.append(f"{page.relative_to(ROOT)}: image {name}.svg needs alt text")
            src, svg = SRC / f"{name}.mmd", IMAGES / f"{name}.svg"
            if not src.exists():
                problems.append(f"{page.relative_to(ROOT)}: no source images/src/{name}.mmd")
            elif not svg.exists():
                problems.append(f"images/{name}.svg missing; run diagrams.py render")
            elif hashes.get(src.name) != digest(src):
                problems.append(f"images/{name}.svg is stale; run diagrams.py render")
    for p in problems:
        print(f"error: {p}")
    print(f"{len(list(SRC.glob('*.mmd')))} diagram sources, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    sys.exit({"extract": lambda: extract() or 0, "render": lambda: render() or 0, "sync-alt": lambda: sync_alt() or 0, "check": check}[cmd]())
