"""Lab 3.3: what each context strategy costs, and what it forgets.

Simulates a 40-turn agent session. Each turn: a user message (100 tokens), a tool call and
its result (2,000 tokens), and an assistant reply (200 tokens). Facts the agent must keep:
  - a constraint the user states in turn 1 ("budget is 5,000")
  - a constraint the user states in turn 15 ("exclude supplier X")
  - an ID that appears only inside the tool result of turn 8
Strategies are applied before every model call. "clear_tools+notes" also lets the agent write
the ID to a short notes file (60 tokens) kept in context, Anthropic's "structured note-taking". Summarisation keeps each fact with
probability KEEP_P per pass (an assumption; real summaries vary).
numpy only, seeded.
"""
import numpy as np

TURNS, SYSTEM = 40, 1_500
USER, TOOL, REPLY = 100, 2_000, 200
FACTS = {"turn-1 constraint": (1, "user"), "turn-15 constraint": (15, "user"), "turn-8 tool ID": (8, "tool")}
KEEP_P, SUMMARY_TOKENS, TRIGGER, NOTE_TOKENS = 0.9, 800, 30_000, 60
rng = np.random.default_rng(7)


def run(strategy, trials=2_000):
    totals, peaks, kept = [], [], {f: 0 for f in FACTS}
    for _ in range(trials if strategy == "summarise" else 1):
        # history: list of (turn, kind, tokens); summary carries surviving facts
        hist, summary, alive, total, peak = [], 0, set(FACTS), 0, 0
        for t in range(1, TURNS + 1):
            hist += [(t, "user", USER), (t, "tool", TOOL), (t, "reply", REPLY)]
            if strategy == "window":            # keep the last 10 turns
                hist = [m for m in hist if m[0] > t - 10]
            elif strategy in ("clear_tools", "clear_tools+notes"):  # keep only the last 3 tool results
                tool_turns = sorted({m[0] for m in hist if m[1] == "tool"})[-3:]
                hist = [m for m in hist if m[1] != "tool" or m[0] in tool_turns]
            elif strategy == "summarise":       # compact everything but the last 3 turns
                size = SYSTEM + summary + sum(m[2] for m in hist)
                if size > TRIGGER:
                    old = [m for m in hist if m[0] <= t - 3]
                    for f, (ft, _) in FACTS.items():
                        if f in alive and (any(m[0] == ft for m in old) or summary):
                            if rng.random() > KEEP_P:
                                alive.discard(f)
                    hist = [m for m in hist if m[0] > t - 3]
                    summary = SUMMARY_TOKENS
            notes = NOTE_TOKENS if strategy == "clear_tools+notes" and t >= 8 else 0
            ctx = SYSTEM + summary + notes + sum(m[2] for m in hist)
            total += ctx
            peak = max(peak, ctx)
        if strategy != "summarise":
            alive = {f for f, (ft, kind) in FACTS.items() if any(m[0] == ft and m[1] == kind for m in hist)}
            if strategy == "clear_tools+notes":
                alive.add("turn-8 tool ID")   # the agent wrote it to its notes when it saw it
        totals.append(total); peaks.append(peak)
        for f in alive:
            kept[f] += 1
    n = len(totals)
    return np.mean(totals), np.mean(peaks), {f: kept[f] / n for f in FACTS}


print(f"{'strategy':<18}{'input tokens, whole session':>28}{'peak context':>14}   facts still present at turn 40")
base = None
for s in ["keep_all", "window", "clear_tools", "clear_tools+notes", "summarise"]:
    total, peak, kept = run(s)
    base = base or total
    facts = ", ".join(f"{f} {v:.0%}" for f, v in kept.items())
    print(f"{s:<18}{total:>18,.0f} ({total / base:4.0%}){peak:>14,.0f}   {facts}")
