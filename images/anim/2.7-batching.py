"""2.7: static vs continuous batching on four slots over 16 decode steps, swept by a playhead."""
from lib import Anim, PALETTE, MUTED, LINE, INK, steps_bar, esc

FALLBACK = "dd-3.8-continuous-batching"
ALT = ("Animated: four batch slots over 16 decode steps. With static batching, requests A to D start together; "
       "slots whose request finishes early sit idle until the longest, B, finishes at step 14, so only 4 requests "
       "finish and 36% of slot-steps are idle. With continuous batching, a waiting request joins as soon as a slot "
       "frees up, so 8 requests finish and no slot is idle.")

T = 18.0
SW0, SW1 = 1.0, 14.0           # playhead sweep
STEPS, CELL, GX = 16, 36, 130  # columns, cell width, grid x
ROW = 26
# (slot, start, length, label); requests wait in a queue: E, F, G, H, I, J, K
STATIC = [(0, 0, 6, "A"), (1, 0, 14, "B"), (2, 0, 4, "C"), (3, 0, 9, "D"),
          (0, 14, 5, "E"), (1, 14, 8, "F"), (2, 14, 5, "G"), (3, 14, 7, "H")]
CONT = [(0, 0, 6, "A"), (1, 0, 14, "B"), (2, 0, 4, "C"), (3, 0, 9, "D"),
        (2, 4, 5, "E"), (0, 6, 8, "F"), (2, 9, 5, "G"), (3, 9, 7, "H"),
        (0, 14, 6, "I"), (1, 14, 4, "J"), (2, 14, 6, "K")]


def t_at(step):
    return SW0 + (SW1 - SW0) * step / STEPS


def panel(a, y, title, reqs, idle):
    a.text(20, y + 14, title, size=15, fill=INK, weight="600")
    gy = y + 26
    for s in range(4):
        a.text(GX - 10, gy + s * ROW + 18, f"slot {s + 1}", size=12, anchor="end")
    # idle cells (hatched) under requests
    for s, a0, a1 in idle:
        a.add(f'<rect x="{GX + a0 * CELL}" y="{gy + s * ROW + 2}" width="{(a1 - a0) * CELL}" height="{ROW - 4}" rx="3" fill="url(#hatch)" stroke="{LINE}"/>'
              f'<text x="{GX + (a0 + a1) / 2 * CELL}" y="{gy + s * ROW + 17}" text-anchor="middle" font-size="12" fill="{MUTED}">idle</text>')
    f, st, tc = PALETTE["data"]
    for s, start, length, label in reqs:
        end = min(start + length, STEPS)
        w = (end - start) * CELL - 3
        a.add(f'<rect x="{GX + start * CELL + 1}" y="{gy + s * ROW + 2}" width="{w}" height="{ROW - 4}" rx="4" fill="{f}" stroke="{st}" stroke-width="1.3"/>'
              f'<text x="{GX + start * CELL + 10}" y="{gy + s * ROW + 17}" font-size="13" fill="{tc}" font-weight="600">{esc(label)}</text>')
    # curtain that slides right, revealing the grid as time passes
    gw, gh = STEPS * CELL, 4 * ROW
    mv = a.keyframes([(0, "transform:translateX(0px)"), (SW0, "transform:translateX(0px)"),
                      (SW1, f"transform:translateX({gw}px)"), (a.T, f"transform:translateX({gw}px)")], f"transform:translateX({gw}px);")
    a.add(f'<g clip-path="url(#clip{y})"><rect class="{mv}" x="{GX}" y="{gy}" width="{gw + 2}" height="{gh}" fill="#FFFFFF"/></g>')
    a.add(f'<clipPath id="clip{y}"><rect x="{GX}" y="{gy}" width="{gw + 2}" height="{gh}"/></clipPath>')
    # grid lines on top
    for c in range(STEPS + 1):
        a.add(f'<line x1="{GX + c * CELL}" y1="{gy}" x2="{GX + c * CELL}" y2="{gy + gh}" stroke="#E2E8F0" stroke-width="1"/>')
    a.add(f'<rect x="{GX}" y="{gy}" width="{gw}" height="{gh}" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    # playhead
    ph = a.keyframes([(0, "transform:translateX(0px)"), (SW0, "transform:translateX(0px)"),
                      (SW1, f"transform:translateX({gw}px)"), (a.T, f"transform:translateX({gw}px)")], f"transform:translateX({gw}px);")
    a.add(f'<g class="{a.show(SW0, a.T - 0.5, static=False)}"><line class="{ph}" x1="{GX}" y1="{gy - 4}" x2="{GX}" y2="{gy + gh + 4}" stroke="#7C3AED" stroke-width="2.5"/></g>')
    # finished counter, updating as requests complete
    done = sorted(start + length for _, start, length, _ in reqs if start + length <= STEPS)
    cx = GX + gw + 16
    a.text(cx, gy + 22, "finished", size=12)
    marks = [(0, 0)] + [(st, sum(1 for d in done if d <= st)) for st in sorted(set(done))]
    for k, (step, count) in enumerate(marks):
        on = t_at(step) if k else 0.01
        off = t_at(marks[k + 1][0]) if k + 1 < len(marks) else None
        a.text(cx, gy + 50, str(count), size=26, fill=INK, weight="700",
               cls=a.show(on, off, static=(k + 1 == len(marks)), fade=0.05))
    total = 4 * STEPS
    idle_n = sum(a1 - a0 for _, a0, a1 in idle)
    a.text(cx, gy + 76, f"idle: {round(100 * idle_n / total)}%", size=12, cls=a.show(SW1 + 0.2))
    return gy + gh


def build():
    a = Anim(820, 430, T)
    # time axis
    a.text(GX, 18, "decode steps →", size=12)
    idle_static = [(0, 6, 14), (2, 4, 14), (3, 9, 14)]
    b1 = panel(a, 28, "Static batching", STATIC, idle_static)
    a.text(GX, b1 + 22, "Short requests finish; their slots wait for the longest one (B).", size=13, cls=a.show(t_at(5), a.T - 0.5))
    b2 = panel(a, b1 + 40, "Continuous batching", CONT, [])
    a.text(GX, b2 + 22, "A waiting request joins at the next step after any slot frees up.", size=13, cls=a.show(t_at(5), a.T - 0.5))
    a.text(GX, b2 + 42, "Waiting queue: E F G H I J K …", size=12, fill=MUTED)
    steps_bar(a, b2 + 74, [(20, "Same hardware, same requests: more finished, no idle slots", [(SW1, a.T - 0.5)])])
    return a.svg(ALT)
