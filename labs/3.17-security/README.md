# Lab 3.17: Pin your tools, and see what pinning can't see

Supports section [3.17 Security](../../docs/3-components/3.17-security.md).

**Question:** an agent connects to four tool servers. A reviewer approved their tool definitions on
day 1. On day 30 the servers return slightly different definitions. What does hashing ("pinning") the
approved definitions catch, and what does a keyword scanner for hidden instructions catch?

```sh
python3 tool_pinning.py
```

Standard library only. The two JSON files are the tool lists on day 1 and day 30; edit them freely.

## Prediction (before running)

Pinning will catch the changed `convert_currency` description and the new `send_payment` tool. The
keyword scanner will flag both poisoned descriptions (`add` and `find_slot`).

## Result (run 2026-11-01)

| Tool | Pinning (day 30 vs day 1) | Keyword scan | Actually malicious? |
|---|---|---|---|
| fx/convert_currency | CHANGED: block until re-approved | clean | yes (rug pull) |
| fx/list_currencies | unchanged | clean | no |
| notes/add_note | unchanged | clean | no |
| util/add | unchanged | flagged | yes (poisoned) |
| calendar/find_slot | unchanged | clean | yes (poisoned, plain prose) |
| fx/send_payment | NEW: needs review | clean | new capability |

Prediction partly wrong: the scanner missed `find_slot`, whose instruction is written as polite
company policy with no trigger words.

## What it shows

- **Pinning is cheap and exact, but only for change.** It caught the rug pull and the new payment tool
  with no false alarms. It cannot judge a definition that was already bad when it was approved:
  `find_slot` was poisoned on day 1 and stays "unchanged".
- **Keyword scanning catches the lazy attacks.** The `<IMPORTANT>` block was flagged; the same intent
  in ordinary prose was not. This is the same weakness as any input guardrail
  ([3.2](../../docs/3-components/3.2-input-guardrails.md)): it lowers the rate, not the ceiling.
- **Tool descriptions are untrusted input.** Treat a third-party tool server like a third-party
  dependency: review, pin, re-approve on change, and limit what any tool can do regardless of what
  its description says ([2.4](../../docs/2-trade-offs/2.4-capability-vs-security.md)). Here, the
  BCC instruction only works if the email tool accepts arbitrary recipients.

## Exercises

1. Add a pattern that catches `find_slot`. Then rewrite its description so your pattern misses it
   again. How many rounds before you give up?
2. Change one character of `list_currencies` on day 30. What should the agent do while the change is
   unreviewed: fail closed, or keep the old definition?
3. Which control outside the tool server stops the BCC attack regardless of the description?
