"""README hero: a request travels the path through the primer's components and back as an answer."""
from lib import Anim, PALETTE, MUTED, LINE, INK

FALLBACK = "readme"
ALT = ("Animated: a request travels from the user through the gateway (3.1), input guardrails (3.2) and context "
       "engineering (3.3), then retrieval (3.4 to 3.6) and a workflow or agent (3.9 to 3.11), reaches the model layer "
       "(3.7, 3.8), and returns through output checks (3.12) to the user. Caching, asynchronism, evals, observability "
       "and security (3.13 to 3.17) support the whole path.")

T = 10.0
# name: (x, y, w, h, kind, lines)
N = {
    "user": (20, 40, 110, 50, "human", ["User"]),
    "gw": (170, 40, 140, 50, "control", ["Gateway", "3.1"]),
    "ig": (350, 40, 150, 50, "control", ["Input guardrails", "3.2"]),
    "ce": (540, 40, 200, 50, "tool", ["Context engineering", "3.3"]),
    "rt": (430, 150, 160, 50, "data", ["Retrieval", "3.4–3.6"]),
    "wf": (620, 150, 180, 50, "tool", ["Workflow or agent", "3.9–3.11"]),
    "ml": (540, 260, 200, 50, "model", ["Model layer", "3.7–3.8"]),
    "oc": (300, 260, 170, 50, "control", ["Output checks", "3.12"]),
}
ARRIVE = {"user": [0.4, 7.6], "gw": [1.2], "ig": [2.0], "ce": [2.8], "rt": [3.6], "wf": [3.6], "ml": [4.8], "oc": [6.0]}


def c(n):
    x, y, w, h = N[n][:4]
    return x + w / 2, y + h / 2


def build():
    a = Anim(820, 420, T)
    a.text(20, 22, "One request through an AI system, and the section that covers each step", size=13, weight="600")
    # edges (straight segments between box edges)
    def clip(n, tx, ty):
        """Point where the segment from n's centre towards (tx, ty) leaves n's box."""
        x, y, w, h = N[n][:4]
        cx, cy = c(n)
        dx, dy = tx - cx, ty - cy
        k = min((w / 2) / abs(dx) if dx else 9e9, (h / 2) / abs(dy) if dy else 9e9)
        return cx + dx * k, cy + dy * k

    for p, q in [("user", "gw"), ("gw", "ig"), ("ig", "ce"), ("ce", "rt"), ("ce", "wf"), ("rt", "ml"), ("wf", "ml"), ("ml", "oc")]:
        (x1, y1), (x2, y2) = clip(p, *c(q)), clip(q, *c(p))
        a.line(round(x1), round(y1), round(x2 - (x2 - x1) * 0.02), round(y2 - (y2 - y1) * 0.02))
    a.add(f'<path d="M 300 285 H 75 V 92" fill="none" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#ah)"/>')
    a.text(84, 278, "answer", size=13)

    # travelling request (drawn under the boxes): waypoints (x, y, time)
    def dot(points, color="#7C3AED"):
        x0, y0, _ = points[0]
        fr = [(0, f"transform:translate({x0}px,{y0}px)")]
        fr += [(t, f"transform:translate({x}px,{y}px)") for x, y, t in points]
        fr.append((T, f"transform:translate({points[-1][0]}px,{points[-1][1]}px)"))
        mv = a.keyframes(fr, f"transform:translate({x0}px,{y0}px);")
        vis = a.show(points[0][2], points[-1][2], static=False, fade=0.2)
        a.add(f'<g class="{vis}"><g class="{mv}"><circle r="9" fill="{color}" opacity="0.25"/><circle r="5" fill="{color}"/></g></g>')

    ux, uy = c("user")
    common = [(ux, uy, 0.4), (c("gw")[0], uy, 1.2), (c("ig")[0], uy, 2.0), (c("ce")[0], uy, 2.8)]
    tail = [(c("ml")[0], c("ml")[1], 4.8), (c("ml")[0], c("ml")[1], 5.2), (c("oc")[0], c("oc")[1], 6.0),
            (c("oc")[0], c("oc")[1], 6.3), (75, 285, 7.0), (ux, uy, 7.6)]
    dot(common + [(c("rt")[0], c("rt")[1], 3.6), (c("rt")[0], c("rt")[1], 4.0)] + tail)
    dot([(c("ce")[0], uy, 2.8), (c("wf")[0], c("wf")[1], 3.6), (c("wf")[0], c("wf")[1], 4.0), (c("ml")[0], c("ml")[1], 4.8)])

    # boxes drawn after the dots, so a request disappears inside the step it is in
    for n, (x, y, w, h, kind, lines) in N.items():
        spans = [(t - 0.1, t + 0.6) for t in ARRIVE[n]]
        pulse = a.spans("stroke-width", "1.5", "4", spans, static_active=False)
        a.box(x, y, w, h, kind, lines, extra=pulse, size=15)

    # supporting concerns across the whole path
    a.add(f'<rect x="20" y="340" width="780" height="64" rx="8" fill="#F8FAFC" stroke="{LINE}" stroke-width="1.5"/>')
    a.text(32, 360, "Across the whole path", weight="600")
    chips = [("Caching", "3.13"), ("Async", "3.14"), ("Evals", "3.15"), ("Observability", "3.16"), ("Security", "3.17")]
    f, s, tc = PALETTE["plain"]
    for i, (name, sec) in enumerate(chips):
        x = 32 + i * 152
        t0 = 0.6 + i * 1.5
        glow = a.spans("stroke", LINE, "#7C3AED", [(t0, t0 + 1.4)], static_active=False)
        a.add(f'<rect class="{glow}" x="{x}" y="368" width="140" height="28" rx="6" fill="#FFFFFF" stroke="{LINE}" stroke-width="1.5"/>'
              f'<text x="{x + 70}" y="387" text-anchor="middle" font-size="14" fill="{INK}">{name} <tspan fill="{MUTED}">{sec}</tspan></text>')
    return a.svg(ALT)
