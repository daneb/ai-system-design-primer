"""Lab 3.18: what LoRA trains, and when a fine-tuned small model pays for itself.

Part 1: trainable parameters for LoRA on an 8B-shaped model (32 layers, hidden 4096), adapters on the
four attention projections, for several ranks. (Shapes simplified: all four projections 4096x4096.)
Part 2: break-even monthly volume for replacing a large hosted model with a fine-tuned small one.
All prices are ILLUSTRATIVE. Standard library only.
"""
LAYERS, D, BASE = 32, 4096, 8e9
print("| LoRA rank | Trainable parameters | Share of base model | Adapter size (16-bit) |")
print("|---|---|---|---|")
for r in (4, 8, 16, 64):
    p = LAYERS * 4 * (D * r + r * D)
    print(f"| {r} | {p/1e6:.1f} M | {p/BASE:.3%} | {p*2/1e6:.0f} MB |")

# Part 2 -- per-request tokens: large model needs a 3,000-token few-shot prompt; tuned small needs 300.
REQ_OUT = 200
large = dict(inp=3300, out=REQ_OUT, p_in=3.0, p_out=15.0)       # $ per M tokens
small = dict(inp=600,  out=REQ_OUT, p_in=0.4, p_out=1.6)
def per_req(m): return (m["inp"] * m["p_in"] + m["out"] * m["p_out"]) / 1e6
ONE_OFF = 2_000 + 8_000          # training run(s) + building and labelling the dataset, $
EVAL_PER_UPGRADE = 1_500         # re-validating the tune, $ per base-model upgrade (assume 2 a year)
print(f"\nPer request: large few-shot ${per_req(large)*1000:.2f} per 1k, tuned small ${per_req(small)*1000:.2f} per 1k")
print("\n| Hosting for the tuned model | Monthly fixed cost | Break-even requests per month | At 100k/month: saving per year |")
print("|---|---|---|---|")
for label, fixed in (("pay per token (no hosting fee)", 0), ("dedicated capacity, $5/hour", 5*730), ("dedicated capacity, $20/hour", 20*730)):
    monthly_fixed = fixed + (ONE_OFF / 12) + (EVAL_PER_UPGRADE * 2 / 12)
    saving = per_req(large) - per_req(small)
    be = monthly_fixed / saving
    yr = (100_000 * saving - monthly_fixed) * 12
    print(f"| {label} | ${monthly_fixed:,.0f} | {be:,.0f} | ${yr:,.0f} |")
