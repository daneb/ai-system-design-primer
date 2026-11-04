"""Helpers for animated diagrams (STYLE.md, "Animated diagrams").

Each generator in images/anim/ builds one SVG from these helpers. Animation is pure CSS keyframes, no
script, so it plays inside <img> on GitHub. The base (un-animated) styles always describe one complete,
meaningful frame: that is what shows wherever animation is off. Output is deterministic, so
`diagrams.py check` can regenerate it and compare.
"""

FONT = "Inter, 'Helvetica Neue', Helvetica, Arial, sans-serif"
PALETTE = {  # STYLE.md classes: fill, stroke, text
    "model": ("#EEF2FF", "#4F46E5", "#1E1B4B"),
    "tool": ("#ECFDF5", "#059669", "#064E3B"),
    "data": ("#FFFBEB", "#D97706", "#78350F"),
    "human": ("#F1F5F9", "#475569", "#0F172A"),
    "untrusted": ("#FEF2F2", "#DC2626", "#7F1D1D"),
    "control": ("#F5F3FF", "#7C3AED", "#3B0764"),
    "plain": ("#FFFFFF", "#64748B", "#0F172A"),
}
INK, MUTED, FAINT, LINE = "#0F172A", "#475569", "#94A3B8", "#CBD5E1"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Anim:
    """Collects CSS and SVG elements for one diagram with a loop of `period` seconds."""

    def __init__(self, width, height, period):
        self.w, self.h, self.T = width, height, period
        self.css, self.body, self.n = [], [], 0

    # ---- timing ----------------------------------------------------------------------------------
    def _name(self, prefix):
        self.n += 1
        return f"{prefix}{self.n}"

    def pct(self, t):
        return f"{100 * max(0, min(t, self.T)) / self.T:.2f}%"

    def keyframes(self, frames, base, prefix="k"):
        """frames: [(seconds, 'prop:value; ...')]. base: the static-frame declarations."""
        name = self._name(prefix)
        ks = " ".join(f"{self.pct(t)} {{ {d} }}" for t, d in frames)
        self.css.append(f"@keyframes {name} {{ {ks} }}")
        self.css.append(f".{name} {{ {base} animation: {name} {self.T}s linear infinite; }}")
        return name

    def show(self, on, off=None, static=True, fade=0.35):
        """Class that makes an element visible from `on` to `off` seconds (default: end of loop)."""
        off = self.T - 0.5 if off is None else off
        fr = [(0, "opacity:0"), (on, "opacity:0"), (on + fade, "opacity:1"),
              (off, "opacity:1"), (off + fade, "opacity:0"), (self.T, "opacity:0")]
        return self.keyframes(fr, f"opacity:{1 if static else 0};", "v")

    def spans(self, prop, rest, active, spans, static_active=True):
        """Switch `prop` to `active` during each (start, end) span, `rest` otherwise."""
        fr = [(0, f"{prop}:{rest}")]
        for a, b in spans:
            fr += [(a, f"{prop}:{rest}"), (a + 0.2, f"{prop}:{active}"), (b, f"{prop}:{active}"), (b + 0.2, f"{prop}:{rest}")]
        fr.append((self.T, f"{prop}:{rest}"))
        return self.keyframes(fr, f"{prop}:{active if static_active else rest};", "s")

    def move(self, dx, dy, t_start, t_end, static_at_end=True):
        """Translate from (dx, dy) to (0, 0) between t_start and t_end."""
        fr = [(0, f"transform:translate({dx}px,{dy}px)"), (t_start, f"transform:translate({dx}px,{dy}px)"),
              (t_end, "transform:translate(0px,0px)"), (self.T, "transform:translate(0px,0px)")]
        base = "transform:translate(0px,0px);" if static_at_end else f"transform:translate({dx}px,{dy}px);"
        return self.keyframes(fr, base, "m")

    def grow_x(self, t_start, t_end):
        fr = [(0, "transform:scaleX(0)"), (t_start, "transform:scaleX(0)"), (t_end, "transform:scaleX(1)"), (self.T, "transform:scaleX(1)")]
        return self.keyframes(fr, "transform-box:fill-box; transform-origin:left;", "g")

    # ---- drawing ---------------------------------------------------------------------------------
    def add(self, s):
        self.body.append(s)

    def text(self, x, y, s, size=13, fill=MUTED, anchor="start", weight=None, cls=""):
        w = f' font-weight="{weight}"' if weight else ""
        c = f' class="{cls}"' if cls else ""
        self.add(f'<text{c} x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{w}>{esc(s)}</text>')

    def box(self, x, y, w, h, kind, lines, cls="", size=15, rx=8, dashed=False, extra=""):
        f, s, t = PALETTE[kind]
        d = ' stroke-dasharray="5 3"' if dashed or kind == "untrusted" else ""
        out = [f'<g class="{cls}">' if cls else "<g>",
               f'<rect class="{extra}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}" stroke="{s}" stroke-width="1.5"{d}/>']
        n = len(lines)
        for i, ln in enumerate(lines):
            yy = y + h / 2 + (i - (n - 1) / 2) * (size + 3) + size * 0.35
            sz = size if i == 0 else size - 2
            wt = ' font-weight="600"' if i == 0 and n > 1 else ""
            out.append(f'<text x="{x + w / 2:g}" y="{yy:.1f}" text-anchor="middle" font-size="{sz}" fill="{t}"{wt}>{esc(ln)}</text>')
        out.append("</g>")
        self.add("".join(out))

    def line(self, x1, y1, x2, y2, cls="", color=MUTED, width=1.5, arrow=True, dashed=False):
        m = ' marker-end="url(#ah)"' if arrow else ""
        d = ' stroke-dasharray="5 3"' if dashed else ""
        c = f' class="{cls}"' if cls else ""
        self.add(f'<line{c} x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"{d}{m}/>')

    def svg(self, title):
        css = " ".join(self.css) + " @media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" '
                f'font-family="{FONT}" role="img">\n<title>{esc(title)}</title>\n<style>{css}</style>\n'
                '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>'
                '<pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                f'<rect width="6" height="6" fill="#F8FAFC"/><line x1="0" y1="0" x2="0" y2="6" stroke="{LINE}" stroke-width="2"/></pattern></defs>\n'
                f'<rect width="{self.w}" height="{self.h}" fill="#FFFFFF"/>\n' + "\n".join(self.body) + "\n</svg>\n")


def steps_bar(a, y, steps):
    """Step captions along the bottom; each lights up during its spans. steps: [(x, label, [(t0, t1)])]."""
    for x, label, spans in steps:
        cls = a.spans("fill", "#64748B", INK, spans)
        a.text(x, y, label, size=14, weight="600", cls=cls)
