#!/usr/bin/env python3
"""Diagram pipeline: Mermaid sources in images/src/*.mmd -> rendered SVGs in images/*.svg.

  python3 scripts/diagrams.py extract   # one-off: move ```mermaid blocks out of pages into images/src
  python3 scripts/diagrams.py render    # render every .mmd with the shared theme (needs Node: npx mmdc)
  python3 scripts/diagrams.py sync-alt  # copy each source's alt line into the pages that show it
  python3 scripts/diagrams.py animate   # build every animated SVG from its generator in images/anim (Python only)
  python3 scripts/diagrams.py check     # alt text, a source, an up-to-date SVG, and text readable at GitHub width

Each .mmd starts with '%% alt: <text>' (the image's alt text). The renderer prepends the shared
classDefs (STYLE.md, "Diagrams") to flowcharts, so sources can use 'class X model' etc. The SHA-256 of
each rendered source is kept in images/.hashes.json so CI can spot a stale SVG without running Node.

Rendered SVGs get explicit pixel sizes (Mermaid writes width="100%", which makes browsers stretch every
diagram to the page width), so all diagrams show 15 px text at natural size. A diagram wider than
MAX_WIDTH is shrunk to fit a GitHub page and its text drops below about 11 px: `check` fails, and the
fix is a narrower layout (top-to-bottom flow, fewer nodes per row), not a smaller font.

Animated diagrams (STYLE.md, "Animated diagrams") are built by Python generators in images/anim/<stem>.py
into images/anim/<stem>.svg. A page shows one in a <picture> whose reduced-motion source is a static
Mermaid diagram, so readers who turn motion off, and print and PDF, get the still version. Generators are
deterministic, so `check` rebuilds each one in memory and fails if the committed SVG differs.
"""
import hashlib, json, pathlib, re, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMAGES, SRC = ROOT / "images", ROOT / "images" / "src"
ANIM = IMAGES / "anim"
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
PICTURE = re.compile(r'<picture>\s*<source media="\(prefers-reduced-motion: reduce\)" srcset="(?:\.\./)*images/([\w.\-]+)\.svg">'
                     r'\s*<img src="(?:\.\./)*images/anim/([\w.\-]+)\.svg" alt="([^"]*)">\s*</picture>')


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


COLUMN, FONT_PX, MIN_PX = 830, 15, 11          # GitHub's content width; theme font size; smallest readable
MAX_WIDTH = int(COLUMN * FONT_PX / MIN_PX)     # 1,131 px


def svg_size(svg_text):
    w, h = re.search(r'viewBox="[-\d.]+ [-\d.]+ ([\d.]+) ([\d.]+)"', svg_text).groups()
    return float(w), float(h)


def fix_size(path):
    """Replace Mermaid's width="100%" with the diagram's real size, so it renders at natural scale."""
    s = path.read_text(encoding="utf-8")
    w, h = svg_size(s)
    tag = re.search(r"<svg\b[^>]*>", s).group(0)
    new = re.sub(r'\s(width|height)="[^"]*"', "", tag)
    new = re.sub(r"max-width:\s*[\d.]+px;?\s*", "", new)
    new = new.replace("<svg", f'<svg width="{w:g}" height="{h:g}"', 1)
    path.write_text(s.replace(tag, new, 1), encoding="utf-8")


def render(only=None):
    mmdc = shutil.which("mmdc")
    cmd = [mmdc] if mmdc else ["npx", "-y", "@mermaid-js/mermaid-cli"]
    hashes = json.loads(HASHES.read_text()) if HASHES.exists() else {}
    tmp = IMAGES / ".tmp.mmd"
    for src in sorted(SRC.glob("*.mmd")):
        if only and src.stem not in only:
            continue
        tmp.write_text(with_classdefs(src.read_text(encoding="utf-8")), encoding="utf-8")
        out = IMAGES / f"{src.stem}.svg"
        r = subprocess.run(cmd + ["-i", str(tmp), "-o", str(out), "-c", str(CONFIG), "-b", "white"],
                           capture_output=True, text=True)
        if r.returncode:
            print(f"FAILED {src.name}\n{r.stderr[-800:]}")
            continue
        fix_size(out)
        hashes[src.name] = digest(src)
        w, _ = svg_size(out.read_text(encoding="utf-8"))
        note = "" if w <= MAX_WIDTH else f"  (too wide: {w:.0f} px > {MAX_WIDTH}; text will be under {MIN_PX} px)"
        print(f"rendered {out.relative_to(ROOT)}{note}")
    tmp.unlink(missing_ok=True)
    HASHES.write_text(json.dumps(hashes, indent=1, sort_keys=True) + "\n")


def generator(stem):
    """Load images/anim/<stem>.py; it defines FALLBACK, ALT and build() -> SVG text."""
    import importlib.util
    sys.dont_write_bytecode = True
    if str(ANIM) not in sys.path:
        sys.path.insert(0, str(ANIM))
    spec = importlib.util.spec_from_file_location(f"anim_{stem}", ANIM / f"{stem}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def generators():
    return sorted(f.stem for f in ANIM.glob("*.py") if f.stem != "lib")


def animate():
    for stem in generators():
        svg = generator(stem).build()
        (ANIM / f"{stem}.svg").write_text(svg, encoding="utf-8")
        w, _ = svg_size(svg)
        note = f"  (too wide: {w:.0f} px > {MAX_WIDTH})" if w > MAX_WIDTH else ""
        print(f"animated images/anim/{stem}.svg{note}")


def attr(text):
    import html
    return html.escape(text, quote=True)


def check_picture(page, static, anim, alt):
    import html
    rel, out = page.relative_to(ROOT), []
    gen = ANIM / f"{anim}.py"
    if not gen.exists():
        return [f"{rel}: no generator images/anim/{anim}.py"]
    mod = generator(anim)
    if mod.FALLBACK != static:
        out.append(f"{rel}: images/anim/{anim}.py falls back to {mod.FALLBACK}, but the page uses {static}")
    if html.unescape(alt) != mod.ALT:
        out.append(f"{rel}: alt text for images/anim/{anim}.svg is out of date; run diagrams.py sync-alt")
    if len(mod.ALT) < 15:
        out.append(f"images/anim/{anim}.py needs ALT text")
    svg = ANIM / f"{anim}.svg"
    built = mod.build()
    if not svg.exists() or svg.read_text(encoding="utf-8") != built:
        out.append(f"images/anim/{anim}.svg is missing or stale; run diagrams.py animate")
    w, _ = svg_size(built)
    if w > MAX_WIDTH:
        out.append(f"images/anim/{anim}.svg is {w:.0f} px wide (max {MAX_WIDTH})")
    return out


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
        new = PICTURE.sub(lambda m: m.group(0).replace(f'alt="{m.group(3)}"', f'alt="{attr(generator(m.group(2)).ALT)}"'), new)
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
        static = [(n, n) for n, _, _ in PICTURE.findall(text)]
        for name, anim, alt in PICTURE.findall(text):
            problems += check_picture(page, name, anim, alt)
        for alt, link, name in IMG.findall(text) + [("static fallback for an animation", "", n) for n, _ in static]:
            if len(alt.strip()) < 15:
                problems.append(f"{page.relative_to(ROOT)}: image {name}.svg needs alt text")
            src, svg = SRC / f"{name}.mmd", IMAGES / f"{name}.svg"
            if not src.exists():
                problems.append(f"{page.relative_to(ROOT)}: no source images/src/{name}.mmd")
            elif not svg.exists():
                problems.append(f"images/{name}.svg missing; run diagrams.py render")
            elif hashes.get(src.name) != digest(src):
                problems.append(f"images/{name}.svg is stale; run diagrams.py render")
            else:
                w, _ = svg_size(svg.read_text(encoding="utf-8"))
                if w > MAX_WIDTH:
                    problems.append(f"images/{name}.svg is {w:.0f} px wide; on a GitHub page its text "
                                    f"shrinks below {MIN_PX} px. Use a narrower layout (max {MAX_WIDTH} px)")
    for p in problems:
        print(f"error: {p}")
    print(f"{len(list(SRC.glob('*.mmd')))} diagram sources, {len(generators())} animations, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    sys.exit({"extract": lambda: extract() or 0, "render": lambda: render(set(sys.argv[2:]) or None) or 0, "sync-alt": lambda: sync_alt() or 0, "animate": lambda: animate() or 0, "check": check}[cmd]())
