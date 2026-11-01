"""Lab 2.4: audit agents against the Rule of Two, then size the residual risk.

Part 1 reads agents.json and marks each agent with the properties its tools give it:
  A = processes untrusted input, B = touches sensitive data, C = changes state or communicates out.
An agent with all three in one session is flagged.

Part 2 asks: if we rely on a detector instead of architecture, how many injections succeed?
Standard library only.
"""
import argparse, json, pathlib

def audit(path):
    cfg = json.loads(pathlib.Path(path).read_text())
    tools = cfg["tools"]
    print("| Agent | Tools | A untrusted | B sensitive | C acts | Verdict |")
    print("|---|---|---|---|---|---|")
    for name, ts in cfg["agents"].items():
        a = any(tools[t]["untrusted_input"] for t in ts)
        b = any(tools[t]["sensitive"] for t in ts)
        c = any(tools[t]["acts"] for t in ts)
        n = a + b + c
        verdict = "**all three: redesign or gate C**" if n == 3 else f"{n} of 3"
        mark = lambda x: "yes" if x else "-"
        print(f"| {name} | {', '.join(ts)} | {mark(a)} | {mark(b)} | {mark(c)} | {verdict} |")

def residual(sessions, items, attack_rate, misses):
    print("\n| Detector miss rate | P(session compromised) | Compromised sessions per day |")
    print("|---|---|---|")
    for miss in misses:
        p_item = attack_rate * miss
        p_session = 1 - (1 - p_item) ** items
        print(f"| {miss:.0%} | {p_session:.4%} | {sessions * p_session:,.0f} |")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=pathlib.Path(__file__).with_name("agents.json"))
    ap.add_argument("--sessions", type=int, default=100_000)
    ap.add_argument("--items", type=int, default=20, help="untrusted items read per session")
    ap.add_argument("--attack-rate", type=float, default=0.001, help="share of items carrying an injection")
    a = ap.parse_args()
    audit(a.config)
    residual(a.sessions, a.items, a.attack_rate, [0.5, 0.1, 0.01])
