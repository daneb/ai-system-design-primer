"""0.2: prefill reads the whole prompt in one pass; decode writes one token per step, reading all the
weights and the KV cache each time; a reasoning model's first tokens are hidden reasoning."""
from lib import Anim, PALETTE, MUTED, LINE, FAINT, steps_bar, esc

FALLBACK = "0.2-inside-a-model-call"
ALT = ("Animated: six prompt tokens enter the model together in one prefill pass, which keeps the arithmetic busy, "
       "fills six KV-cache entries and produces the first token. Then decode writes one token per step; each step "
       "reads all 16 GB of weights and the KV cache from memory, adds one cache entry and one output token. "
       "The first two output tokens are hidden reasoning, billed as output; the rest is the visible answer.")

T = 17.0
PRE0, PRE1 = 1.0, 2.6            # prefill pass
DEC = [4.0, 5.6, 7.2, 8.8, 10.4]  # decode steps (each produces one token)
END = 13.5
PROMPT = ["Summarise", "␣the", "␣contract", "␣in", "␣three", "␣bullets"]
OUT = [("think", True), ("think", True), ("•␣Pay", False), ("␣in", False), ("␣30", False), ("␣days", False)]
CW, CG = 104, 8          # prompt chip width, gap
OX, OW = 36, 92          # output chip x0, width+gap


def chip(a, x, y, w, label, kind, cls="", dashed=False):
    f, s, t = PALETTE[kind]
    d = ' stroke-dasharray="4 3"' if dashed else ""
    a.add(f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="32" rx="6" fill="{f}" stroke="{s}" stroke-width="1.5"{d}/>'
          f'<text x="{x + w / 2}" y="{y + 21}" text-anchor="middle" font-size="14" fill="{t}" font-weight="600">{esc(label)}</text></g>')


def meter(a, x, y, label, spans_hi):
    """A horizontal meter that fills during each span."""
    a.text(x, y, label, size=12)
    a.add(f'<rect x="{x}" y="{y + 6}" width="150" height="10" rx="5" fill="#F1F5F9" stroke="{LINE}"/>')
    fr = [(0, "transform:scaleX(0.05)")]
    for s0, s1 in spans_hi:
        fr += [(s0, "transform:scaleX(0.05)"), (s0 + 0.15, "transform:scaleX(1)"), (s1, "transform:scaleX(1)"), (s1 + 0.25, "transform:scaleX(0.05)")]
    fr.append((T, "transform:scaleX(0.05)"))
    cls = a.keyframes(fr, "transform:scaleX(0.05); transform-box:fill-box; transform-origin:left;")
    a.add(f'<rect class="{cls}" x="{x}" y="{y + 6}" width="150" height="10" rx="5" fill="#4F46E5"/>')


def build():
    a = Anim(820, 500, T)
    # prompt row
    a.text(20, 24, "Prompt (input tokens)", weight="600")
    px = [20 + i * (CW + CG) for i in range(len(PROMPT))]
    for x, tok in zip(px, PROMPT):
        chip(a, x, 34, CW, tok, "data")
    # model
    MX, MY, MW, MH = 250, 120, 320, 64
    a.add(f'<rect x="{MX}" y="{MY}" width="{MW}" height="{MH}" rx="8" fill="{PALETTE["model"][0]}" stroke="{PALETTE["model"][1]}" stroke-width="1.5"/>')
    a.text(MX + MW / 2, MY + 28, "Model", size=15, fill=PALETTE["model"][2], anchor="middle", weight="600")
    a.text(MX + MW / 2, MY + 47, "8B parameters: 16 GB of weights", size=13, fill=PALETTE["model"][2], anchor="middle")
    # prefill: every prompt token flows into the model at once
    pre = a.spans("opacity", "0.15", "1", [(PRE0, PRE1)], static_active=False)
    for x in px:
        a.line(x + CW / 2, 66, MX + MW / 2 + (x + CW / 2 - 330) * 0.25, MY - 2, cls=pre, color="#4F46E5")
    a.text(MX + MW + 14, 96, "Prefill: all prompt tokens", fill=PALETTE["model"][2], weight="600", cls=a.show(PRE0, PRE1 + 0.6, static=False))
    a.text(MX + MW + 14, 112, "in one parallel pass", fill=PALETTE["model"][2], cls=a.show(PRE0, PRE1 + 0.6, static=False))
    dec_spans = [(t - 0.5, t + 0.2) for t in DEC]
    a.text(MX + MW + 14, 96, "Decode: one token per step,", fill=PALETTE["model"][2], weight="600", cls=a.show(DEC[0] - 0.6, END))
    a.text(MX + MW + 14, 112, "rereading weights and cache", fill=PALETTE["model"][2], cls=a.show(DEC[0] - 0.6, END))
    # meters
    meter(a, 20, 120, "Arithmetic busy", [(PRE0, PRE1)])
    meter(a, 20, 156, "Memory reads", [(PRE0, PRE1)] + dec_spans)

    # KV cache
    KY = 232
    a.add(f'<rect x="20" y="{KY}" width="780" height="70" rx="8" fill="#F8FAFC" stroke="{LINE}" stroke-width="1.5"/>')
    a.text(32, KY + 20, "KV cache: one entry per token, about 131 KB each", weight="600")
    for i in range(12):
        x = 32 + i * 63
        a.add(f'<rect x="{x}" y="{KY + 30}" width="56" height="28" rx="4" fill="none" stroke="{LINE}" stroke-dasharray="3 3"/>')
        if i < 6:
            on = PRE1 - 0.4
        elif i - 6 < len(DEC):
            on = DEC[i - 6] - 0.2
        else:
            continue
        static = i < 11
        f, s, _ = PALETTE["data"]
        a.add(f'<rect class="{a.show(on, END, static)}" x="{x}" y="{KY + 30}" width="56" height="28" rx="4" fill="{f}" stroke="{s}" stroke-width="1.5"/>')
    # model <-> cache arrows
    a.line(MX + 80, MY + MH, MX + 80, KY - 2, cls=a.spans("opacity", "0.2", "1", [(PRE1 - 0.6, PRE1)] + [(t - 0.3, t) for t in DEC], static_active=True), color="#4F46E5")
    a.line(MX + 120, KY, MX + 120, MY + MH + 2, cls=a.spans("opacity", "0.2", "1", dec_spans), color="#4F46E5")
    a.text(MX + 128, MY + MH + 30, "read on every decode step", size=12, cls=a.show(DEC[0] - 0.6, END))
    a.text(MX + 72, MY + MH + 30, "write", size=12, anchor="end")

    # output row
    OY = 352
    a.text(20, OY - 12, "Output tokens (billed at the output price)", weight="600")
    a.add(f'<path d="M {MX + MW} {MY + MH / 2} H 806 V {OY + 16} H 594" fill="none" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#ah)"/>')
    for i, (tok, hidden) in enumerate(OUT):
        x = OX + i * OW
        on = PRE1 if i == 0 else DEC[i - 1]
        kind = "human" if hidden else "tool"
        chip(a, x, OY, 84, "···" if hidden else tok, kind, cls=a.show(on, END, True), dashed=hidden)
    a.add(f'<path d="M {OX} {OY + 44} h {2 * OW - 8}" stroke="{FAINT}" stroke-width="1.5" fill="none"/>')
    a.text(OX, OY + 60, "hidden reasoning", size=12, cls=a.show(DEC[0] + 0.2, END))
    a.add(f'<path d="M {OX + 2 * OW} {OY + 44} h {4 * OW - 8}" stroke="{PALETTE["tool"][1]}" stroke-width="1.5" fill="none"/>')
    a.text(OX + 2 * OW, OY + 60, "visible answer, streamed", size=12, cls=a.show(DEC[1] + 0.2, END))

    # timing brackets
    tx = OX + 6 * OW + 18
    a.text(tx, OY + 60, "first token after prefill:", size=12, cls=a.show(PRE1, DEC[0] - 0.5, static=False))
    a.text(tx, OY + 76, "time to first token", size=12, weight="600", cls=a.show(PRE1, DEC[0] - 0.5, static=False))
    a.text(tx, OY + 60, "then one per step:", size=12, cls=a.show(DEC[0] + 0.1, END))
    a.text(tx, OY + 76, "time per output token", size=12, weight="600", cls=a.show(DEC[0] + 0.1, END))

    steps_bar(a, 482, [(20, "1  Prefill: whole prompt in one pass, limited by arithmetic", [(PRE0, DEC[0] - 0.6)]),
                       (470, "2  Decode: one token per step, limited by memory", [(DEC[0] - 0.6, END)])])
    return a.svg(ALT)
