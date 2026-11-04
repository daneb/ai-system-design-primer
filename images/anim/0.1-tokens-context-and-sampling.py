"""0.1: tokenize, score every next token, keep the top-p set, pick one, append, repeat."""
from lib import Anim, PALETTE, MUTED, LINE, steps_bar, esc

FALLBACK = "0.1-tokens-context-and-sampling"
ALT = ("Animated: “The cat sat on the” is split into five tokens with IDs, which fill the context window. "
       "The model gives a probability for every possible next token. Top-p 0.8 keeps the likeliest three, "
       "and the sampler picks “ mat”, which is appended to the context. The loop runs again and appends a full stop.")

T = 16.0
TOK0, TOKD = 1.0, 0.45
MODEL1, BARS1, CUT1, PICK1, FLY1 = 3.8, 4.4, 5.6, 6.6, 7.4
MODEL2, BARS2, CUT2, PICK2, FLY2 = 9.0, 9.4, 10.4, 11.2, 12.0
CTX_Y = 128


def slot(i):
    return 36 + i * 94


def chip(a, x, y, tok, tid, kind="data", cls=""):
    f, s, t = PALETTE[kind]
    a.add(f'<g class="{cls}"><rect x="{x}" y="{y}" width="86" height="44" rx="6" fill="{f}" stroke="{s}" stroke-width="1.5"/>'
          f'<text x="{x + 43}" y="{y + 20}" text-anchor="middle" font-size="15" fill="{t}" font-weight="600">{esc(tok)}</text>'
          f'<text x="{x + 43}" y="{y + 36}" text-anchor="middle" font-size="12" fill="{t}">{tid}</text></g>')


def bars(a, rows, t_bars, t_cut, t_pick, t_end, keep, static):
    for j, (tok, p) in enumerate(rows):
        y = 262 + j * 25
        t0 = t_bars + j * 0.08
        w = round(p / 0.6 * 200)
        vis = a.show(t0, t_end, static)
        dim = "" if j < keep else a.keyframes([(0, "opacity:1"), (t_cut, "opacity:1"), (t_cut + 0.4, "opacity:0.25"), (T, "opacity:0.25")], "opacity:0.25;")
        grow = a.grow_x(t0, t0 + 0.6)
        pick = a.keyframes([(0, "fill:#94A3B8"), (t_pick, "fill:#94A3B8"), (t_pick + 0.3, "fill:#7C3AED"), (T, "fill:#7C3AED")], "fill:#7C3AED;") if j == 0 else ""
        fill = "" if pick else ' fill="#94A3B8"'
        val = a.show(t0 + 0.5, t_end, static)
        a.add(f'<g class="{vis}"><g class="{dim}">'
              f'<text x="296" y="{y + 13}" text-anchor="end" font-size="14" fill="#1E293B">{esc(tok)}</text>'
              f'<g class="{grow}"><rect class="{pick}" x="304" y="{y + 2}" width="{w}" height="15" rx="3"{fill}/></g>'
              f'<text class="{val}" x="{304 + w + 6}" y="{y + 14}" font-size="13" fill="{MUTED}">{p:.2f}</text></g></g>')
    yb, ye = 262, 262 + keep * 25 - 6
    cut = a.show(t_cut, t_end, static)
    a.add(f'<g class="{cut}"><path d="M 566 {yb} h 8 V {ye} h -8" fill="none" stroke="#7C3AED" stroke-width="1.5"/>'
          f'<text x="580" y="{(yb + ye) / 2 - 3}" font-size="12" fill="#3B0764">top-p</text>'
          f'<text x="580" y="{(yb + ye) / 2 + 11}" font-size="12" fill="#3B0764">0.8</text></g>')
    a.text(228, 262 + len(rows) * 25 + 14, "… and about 100,000 more, each with a tiny probability", size=12, fill="#64748B",
           cls=a.show(t_bars + 0.6, t_end, static))


def fly(a, i, tok, tid, t_pick, t_fly, static):
    vis = a.show(t_pick + 0.2, None, static, fade=0.3)
    mv = a.move(680 - slot(i), 280 - CTX_Y, t_fly, t_fly + 0.9)
    a.add(f'<g class="{vis}"><g class="{mv}">')
    chip(a, slot(i), CTX_Y, tok, tid, "control")
    a.add("</g></g>")


def build():
    a = Anim(820, 470, T)
    a.box(20, 20, 250, 48, "data", ["“The cat sat on the”"])
    a.line(270, 44, 318, 44)
    a.box(320, 20, 140, 48, "tool", ["Tokenizer"])
    a.text(480, 49, "splits text into tokens, each with an ID")
    a.line(390, 68, 390, 98)
    a.add(f'<rect x="20" y="100" width="780" height="86" rx="8" fill="#F8FAFC" stroke="{LINE}" stroke-width="1.5"/>')
    a.text(32, 120, "Context window", weight="600")
    for i in range(7):
        a.add(f'<rect x="{slot(i)}" y="{CTX_Y}" width="86" height="44" rx="6" fill="none" stroke="{LINE}" stroke-dasharray="4 3"/>')
    for i, (tk, tid) in enumerate([("The", 791), ("␣cat", 8415), ("␣sat", 7731), ("␣on", 389), ("␣the", 279)]):
        chip(a, slot(i), CTX_Y, tk, tid, cls=a.show(TOK0 + i * TOKD))
    a.text(790, 120, "5 tokens used", anchor="end", cls=a.show(TOK0 + 4 * TOKD, FLY1 + 0.6))
    a.text(790, 120, "6 tokens used", anchor="end", cls=a.show(FLY1 + 0.6, FLY2 + 0.6, static=False))
    a.text(790, 120, "7 tokens used", anchor="end", cls=a.show(FLY2 + 0.6, static=False))

    a.line(100, 186, 100, 236)
    a.text(108, 216, "all tokens, every step")
    pulse = a.keyframes([(0, "stroke-width:1.5")] + [x for m in (MODEL1, MODEL2) for x in
                        ((m, "stroke-width:1.5"), (m + 0.3, "stroke-width:5"), (m + 0.9, "stroke-width:1.5"))] + [(T, "stroke-width:1.5")], "")
    a.box(20, 238, 160, 56, "model", ["Model"], extra=pulse)
    a.line(180, 266, 214, 266)
    a.add(f'<rect x="216" y="226" width="400" height="190" rx="8" fill="#FFFFFF" stroke="{LINE}" stroke-width="1.5"/>')
    a.text(228, 246, "Probability of every possible next token", weight="600")
    bars(a, [("␣mat", 0.46), ("␣floor", 0.22), ("␣sofa", 0.12), ("␣bed", 0.08), ("␣roof", 0.04)], BARS1, CUT1, PICK1, MODEL2 - 0.3, 3, True)
    bars(a, [(".", 0.55), ("␣and", 0.15), (",", 0.12), ("␣while", 0.05), ("␣again", 0.03)], BARS2, CUT2, PICK2, T - 0.5, 3, False)

    a.line(616, 300, 642, 300)
    a.box(644, 262, 156, 76, "control", ["Sampler", "picks one at random,", "weighted by probability"], size=15)
    a.add(f'<path d="M 722 262 V 200" fill="none" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#ah)"/>')
    a.text(730, 236, "append,")
    a.text(730, 252, "repeat")
    fly(a, 5, "␣mat", 2450, PICK1, FLY1, True)
    fly(a, 6, ".", 13, PICK2, FLY2, False)

    steps_bar(a, 452, [(20, "1  Tokenize", [(TOK0, MODEL1)]),
                       (150, "2  Model scores every token", [(MODEL1, CUT1), (MODEL2, CUT2)]),
                       (370, "3  Keep the top-p set, pick one", [(CUT1, FLY1), (CUT2, FLY2)]),
                       (620, "4  Append and repeat", [(FLY1, MODEL2), (FLY2, T - 0.5)])])
    a.text(800, 12, "IDs and probabilities illustrative", size=11, fill="#94A3B8", anchor="end")
    return a.svg(ALT)
