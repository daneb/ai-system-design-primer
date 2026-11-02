"""Lab 0.3: the tool-calling loop, what it costs in tokens, and what schema checking catches.

Part 1: an agent loop resends the whole conversation on every call. Count input tokens per call and
in total for a task that needs N tool calls, with a small and a large set of tool definitions.
Part 2: a scripted stand-in for a model proposes 2,000 tool calls; 3% have a malformed argument and
1% name a tool the user may not use. Compare running them as proposed, with schema validation, and
with validation plus a permission check.
Standard library only; seeded. Token sizes are round illustrative numbers.
"""
import random

random.seed(3)
SYSTEM, USER, CALL, RESULT, ANSWER = 400, 60, 40, 300, 200   # tokens per piece

# ---- Part 1 -----------------------------------------------------------------------------------
def loop_tokens(n_calls, tools_tokens):
    history = SYSTEM + tools_tokens + USER
    per_call, total_in, total_out = [], 0, 0
    for _ in range(n_calls):
        per_call.append(history); total_in += history; total_out += CALL
        history += CALL + RESULT                  # the call and its result join the conversation
    per_call.append(history); total_in += history; total_out += ANSWER     # final answer
    return per_call, total_in, total_out

print("| Tool calls | Tool definitions | Input tokens on the last call | Total input tokens | Total output tokens |")
print("|---|---|---|---|---|")
for n in (1, 5, 20):
    for label, tt in (("5 tools (1,000 tokens)", 1000), ("50 tools (10,000 tokens)", 10000)):
        per, tin, tout = loop_tokens(n, tt)
        print(f"| {n} | {label} | {per[-1]:,} | {tin:,} | {tout:,} |")

# ---- Part 2 -----------------------------------------------------------------------------------
SCHEMA = {"get_balance": {"account_id": str},
          "transfer": {"from_id": str, "to_id": str, "amount": float}}
ALLOWED = {"get_balance"}                     # this user's session may only read

def propose():
    r = random.random()
    if r < 0.01:
        return "transfer", {"from_id": "A1", "to_id": "X9", "amount": 5000.0}, "forbidden"
    if r < 0.04:
        bad = random.choice([{"account": "A1"}, {"account_id": 1471}, {}])
        return "get_balance", bad, "malformed"
    return "get_balance", {"account_id": "A1"}, "ok"

def valid(name, args):
    spec = SCHEMA.get(name)
    return spec is not None and set(args) == set(spec) and all(isinstance(args[k], t) for k, t in spec.items())

calls = [propose() for _ in range(2000)]
rows = {"run as proposed": (lambda n, a: True),
        "schema validation": (lambda n, a: valid(n, a)),
        "validation + permission check": (lambda n, a: valid(n, a) and n in ALLOWED)}
print("\n| Policy | Calls executed | Malformed calls reaching the system | Forbidden calls executed | Calls returned to the model as errors |")
print("|---|---|---|---|---|")
for label, gate in rows.items():
    ran = [(n, a, k) for n, a, k in calls if gate(n, a)]
    print(f"| {label} | {len(ran):,} | {sum(k == 'malformed' for *_, k in ran)} | "
          f"{sum(k == 'forbidden' for *_, k in ran)} | {len(calls) - len(ran)} |")

# ---- Chart (optional; needs matplotlib) --------------------------------------------------------
import pathlib as _pl, sys as _sys
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from chart import line_chart
CHART_PATH = _pl.Path(__file__).with_name("result.svg")
ns = list(range(1, 21))
line_chart(CHART_PATH, ns, {"50 tools": [loop_tokens(n, 10000)[1] for n in ns],
                     "5 tools": [loop_tokens(n, 1000)[1] for n in ns]},
           title="Every step resends the history and the tool definitions",
           xlabel="Tool calls in the task", ylabel="Total input tokens", xticks=[1, 5, 10, 15, 20])
