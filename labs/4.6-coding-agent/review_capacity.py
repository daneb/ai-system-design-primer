"""Lab 4.6: merged work is capped by human review, not by how many agent tasks you start.

Each working day the agents open N pull requests. Reviewers have a fixed budget of reviewer-hours a
day. A review round takes 15 minutes; a pull request needs 1-4 rounds (mean 1.6), with the agent's
revision ready the next day. Reviewers take the oldest waiting pull request first. One untouched for
5 working days goes stale (conflicts, the ticket moved on) and is closed: its tokens, sandbox time and
any review already spent are wasted. Optional light lane: 30% of pull requests are low-risk
(dependency bumps with green tests) and take 3-minute reviews.
Standard library only; seeded; 60 working days, the first 20 discarded as warm-up.
"""
import random
from collections import deque

REVIEW_HOURS = 250            # reviewer-hours a day available for agent pull requests
ROUND_MIN, LIGHT_MIN, STALE_DAYS = 15, 3, 5
TASK_COST = 1.21              # $ per agent task (Step 2 of 4.6)
DAYS, WARM = 60, 20

def rounds():
    r = 1
    while random.random() < 0.375 and r < 4:     # mean about 1.6 rounds
        r += 1
    return r

def simulate(n_per_day, light_lane, seed=6):
    random.seed(seed)
    queue, merged, stale, opened = deque(), 0, 0, 0
    for day in range(DAYS):
        for _ in range(n_per_day):
            light = light_lane and random.random() < 0.30
            queue.append({"born": day, "touched": day, "left": rounds(), "light": light, "ready": day})
        if day >= WARM:
            opened += n_per_day
        budget, waiting = REVIEW_HOURS * 60, deque()
        while queue:
            pr = queue.popleft()
            if day - pr["touched"] >= STALE_DAYS:
                stale += day >= WARM; continue
            cost = LIGHT_MIN if pr["light"] else ROUND_MIN
            if pr["ready"] > day or budget < cost:
                waiting.append(pr); continue
            budget -= cost; pr["left"] -= 1; pr["touched"] = day
            if pr["left"] == 0:
                merged += day >= WARM
            else:
                pr["ready"] = day + 1; waiting.append(pr)
        queue = waiting
    days = DAYS - WARM
    return merged / days, stale / max(opened, 1), opened * TASK_COST / max(merged, 1)

print(f"{REVIEW_HOURS} reviewer-hours a day; {ROUND_MIN}-minute review rounds; stale after {STALE_DAYS} days\n")
print("| Agent pull requests a day | Merged a day | Closed as stale | Token cost per merged PR | Merged a day, with light lane |")
print("|---|---|---|---|---|")
tasks = [200, 400, 600, 800, 1000, 1500, 2000, 3000]
std, lane = [], []
for n in tasks:
    m, s, c = simulate(n, False)
    ml, _, _ = simulate(n, True)
    std.append(m); lane.append(ml)
    print(f"| {n:,} | {m:,.0f} | {s:.0%} | ${c:,.2f} | {ml:,.0f} |")

# ---- Chart (optional; needs matplotlib) --------------------------------------------------------
import pathlib as _pl, sys as _sys
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent))
from chart import line_chart
CHART_PATH = _pl.Path(__file__).with_name("result.svg")
line_chart(CHART_PATH, tasks, {"With a light-review lane": lane, "Standard review": std},
           title="Starting more agent tasks stops adding merged work once review is full",
           xlabel="Agent pull requests opened a day", ylabel="Pull requests merged a day",
           xticks=[200, 1000, 2000, 3000])
