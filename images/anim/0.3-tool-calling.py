"""0.3: the tool-calling loop as a sequence that builds up, with the input tokens resent on each call."""
from lib import Anim, PALETTE, MUTED, LINE, INK, steps_bar, esc

FALLBACK = "0.3-tool-calling"
ALT = ("Animated: a user asks for their balance in euros. Your code sends the messages and tool definitions to the model, "
       "which replies with a tool call. Your code checks the schema and the user's permission, runs the tool and sends "
       "everything back with the result, which is untrusted input. A second tool call converts the currency. The model "
       "then gives the final answer. Each call resends the whole conversation, so input tokens grow from 1,200 to 1,480.")

T = 22.0
COL = {"User": 70, "Tool": 210, "Your code": 400, "Model": 620}
KIND = {"User": "human", "Tool": "tool", "Your code": "tool", "Model": "model"}
Y0, DY = 92, 27

# (from, to, label, kind, tokens sent)
MSGS = [
    ("User", "Your code", "Balance in euros?", "human", None),
    ("Your code", "Model", "messages + tool definitions", "tool", 1200),
    ("Model", "Your code", "tool call: get_balance(acct)", "model", None),
    ("Your code", "Your code", "schema valid? user allowed?", "control", None),
    ("Your code", "Tool", "get_balance(acct)", "tool", None),
    ("Tool", "Your code", "R 12,400  (untrusted)", "untrusted", None),
    ("Your code", "Model", "everything again + result", "tool", 1350),
    ("Model", "Your code", "tool call: convert(EUR)", "model", None),
    ("Your code", "Your code", "schema valid? user allowed?", "control", None),
    ("Your code", "Tool", "convert(12400, EUR)", "tool", None),
    ("Tool", "Your code", "€ 640  (untrusted)", "untrusted", None),
    ("Your code", "Model", "everything again + result", "tool", 1480),
    ("Model", "Your code", "final answer (stop: finished)", "model", None),
    ("Your code", "User", "“About €640.”", "human", None),
]
START, STEP = 1.0, 1.15


def build():
    n = len(MSGS)
    end = T - 1.0
    a = Anim(820, Y0 + n * DY + 70, T)
    # lifelines
    for name, x in COL.items():
        f, s, t = PALETTE[KIND[name]]
        w = 110
        a.add(f'<rect x="{x - w / 2}" y="20" width="{w}" height="36" rx="8" fill="{f}" stroke="{s}" stroke-width="1.5"/>'
              f'<text x="{x}" y="43" text-anchor="middle" font-size="15" fill="{t}" font-weight="600">{esc(name)}</text>'
              f'<line x1="{x}" y1="56" x2="{x}" y2="{Y0 + n * DY - 6}" stroke="{LINE}" stroke-width="1.5"/>')
    a.text(805, 34, "Input tokens", anchor="end", weight="600")
    a.text(805, 50, "sent per call", anchor="end")
    a.text(805, 66, "(illustrative)", size=11, fill="#94A3B8", anchor="end")

    for i, (src, dst, label, kind, toks) in enumerate(MSGS):
        y = Y0 + i * DY
        t0 = START + i * STEP
        vis = a.show(t0, end)
        hl = a.spans("opacity", "0.55", "1", [(t0, t0 + STEP)], static_active=True)
        f, s, tc = PALETTE[kind]
        a.add(f'<g class="{vis}"><g class="{hl}">')
        x1, x2 = COL[src], COL[dst]
        if src == dst:  # a check inside your code
            a.add(f'<rect x="{x1 + 8}" y="{y - 12}" width="200" height="20" rx="4" fill="{f}" stroke="{s}" stroke-width="1.2"/>'
                  f'<text x="{x1 + 108}" y="{y + 2}" text-anchor="middle" font-size="12" fill="{tc}">✓ {esc(label)}</text>')
        else:
            dash = ' stroke-dasharray="5 3"' if kind == "untrusted" else ""
            d = 1 if x2 > x1 else -1
            a.add(f'<line x1="{x1 + 4 * d}" y1="{y}" x2="{x2 - 4 * d}" y2="{y}" stroke="{s}" stroke-width="1.6"{dash} marker-end="url(#ah)"/>')
            lx = min(x1, x2) + 14
            a.add(f'<text x="{lx}" y="{y - 5}" font-size="12" fill="{tc}">{esc(label)}</text>')
        if toks:
            w = round(toks / 1500 * 120)
            grow = a.grow_x(t0, t0 + 0.6)
            a.add(f'<rect class="{grow}" x="{805 - 120}" y="{y - 9}" width="{w}" height="12" rx="3" fill="#4F46E5" opacity="0.8"/>'
                  f'<text x="{805 - 124}" y="{y + 1}" font-size="12" fill="{INK}" text-anchor="end" font-weight="600">{toks:,}</text>')
        a.add("</g></g>")

    ys = Y0 + n * DY + 40
    t = lambda i: START + i * STEP  # noqa: E731
    steps_bar(a, ys, [(20, "1  Send messages and tools", [(t(1), t(2)), (t(6), t(7)), (t(11), t(12))]),
                      (232, "2  Model asks for a tool", [(t(2), t(3)), (t(7), t(8))]),
                      (430, "3  Check, run, send back", [(t(3), t(6)), (t(8), t(11))]),
                      (640, "4  Final answer", [(t(12), end)])])
    return a.svg(ALT)
