"""Lab 3.17: pin tool definitions, then see what a pattern scanner catches.

Day 1: a reviewer approves a set of tool definitions (tools_day1.json). We store a hash of each.
Day 30: the servers return tools_day30.json. Pinning reports anything new or changed.
Separately, a keyword scanner looks for hidden instructions in every description.
Standard library only.
"""
import hashlib, json, pathlib, re

HERE = pathlib.Path(__file__).parent
SUSPICIOUS = re.compile(
    r"<important>|ignore (all|previous)|do not (mention|tell)|~/\.ssh|id_rsa|api[_ ]key|password|secret",
    re.I)

def key(t):
    return f"{t['server']}/{t['name']}"

def digest(t):
    return hashlib.sha256(json.dumps(t, sort_keys=True).encode()).hexdigest()[:12]

def main():
    day1 = json.loads((HERE / "tools_day1.json").read_text())
    day30 = json.loads((HERE / "tools_day30.json").read_text())
    pins = {key(t): digest(t) for t in day1}

    print("| Tool | Pinning (day 30 vs day 1) | Keyword scan | Actually malicious? |")
    print("|---|---|---|---|")
    truth = {"fx/convert_currency": "yes (rug pull)", "util/add": "yes (poisoned)",
             "calendar/find_slot": "yes (poisoned, plain prose)", "fx/send_payment": "new capability"}
    for t in day30:
        k = key(t)
        if k not in pins:
            pin = "NEW: needs review"
        elif pins[k] != digest(t):
            pin = "CHANGED: block until re-approved"
        else:
            pin = "unchanged"
        scan = "flagged" if SUSPICIOUS.search(t["description"]) else "clean"
        print(f"| {k} | {pin} | {scan} | {truth.get(k, 'no')} |")

if __name__ == "__main__":
    main()
