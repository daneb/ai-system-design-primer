#!/usr/bin/env python3
"""Lab 3.12: how far does a deterministic quote check get you?

Standard library only. For each claim, check that the quoted text really appears in the cited source
(after normalising whitespace and case). Compare the checker's verdict with the human labels.

Usage: python3 verify_quotes.py
"""
import json
import re
from pathlib import Path


def norm(text):
    return re.sub(r"\s+", " ", text).strip().lower()


def main():
    data = json.loads((Path(__file__).parent / "cases.json").read_text())
    sources = {k: norm(v) for k, v in data["sources"].items()}
    rows, agree = [], 0
    for c in data["claims"]:
        found = norm(c["quote"]) in sources.get(c["source"], "")
        verdict = "pass" if found else "fail"
        human_ok = c["label"].startswith("supported")
        correct = (verdict == "pass") == human_ok
        agree += correct
        rows.append((c["id"], c["text"], verdict, c["label"], "yes" if correct else "NO"))

    print("| Claim | Text | Quote check | Human label | Agrees |")
    print("|---|---|---|---|---|")
    for r in rows:
        print("| " + " | ".join(r) + " |")
    print(f"\nAgreement: {agree}/{len(rows)}")


if __name__ == "__main__":
    main()
