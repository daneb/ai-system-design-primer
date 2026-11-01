# Lab 2.4: Count to three, then size what a detector leaves behind

Supports section [2.4 Capability vs security](../../docs/2-trade-offs/2.4-capability-vs-security.md).

**Question:** which of seven plausible bank agents break the Rule of Two? And if we keep an agent that
does, and lean on an injection detector instead, how many sessions get compromised?

```sh
python3 trifecta.py
python3 trifecta.py --sessions 5000 --items 200   # a document-heavy agent
```

Standard library only. Edit `agents.json` to audit your own tool inventory.

## Prediction (before running)

The two agents that read untrusted content and can send or write (`inbox_assistant`, `kyc_reviewer`)
will be flagged. `support_chat_md` looks read-only, but rendering Markdown loads image URLs in the
user's browser, so it should be flagged too. A good detector will still leave compromised sessions
every day at this volume.

## Result (run 2026-11-01)

| Agent | Tools | A untrusted | B sensitive | C acts | Verdict |
|---|---|---|---|---|---|
| policy_qa | policy_search | - | - | - | 0 of 3 |
| research_helper | web_search, fetch_url | yes | - | yes | 2 of 3 |
| inbox_assistant | read_inbox, send_email | yes | yes | yes | **all three** |
| inbox_summariser | read_inbox | yes | yes | - | 2 of 3 |
| kyc_reviewer | customer_docs_rag, crm_lookup, create_ticket | yes | yes | yes | **all three** |
| kyc_reviewer_split | customer_docs_rag, crm_lookup | yes | yes | - | 2 of 3 |
| support_chat_md | customer_docs_rag, render_markdown | yes | yes | yes | **all three** |

100,000 sessions a day, 20 untrusted items each, 0.1% of items carrying an injection:

| Detector miss rate | P(session compromised) | Compromised sessions per day |
|---|---|---|
| 50% | 0.9953% | 995 |
| 10% | 0.1998% | 200 |
| 1% | 0.0200% | 20 |

Prediction held.

## What it shows

- **Counting is easy; classifying tools is the work.** Most mistakes are in the tool table, not the
  rule: a "read" tool over customer uploads is untrusted input, and a Markdown renderer or `fetch_url`
  is an outbound channel.
- **Splitting fixes it.** `kyc_reviewer_split` drops ticket creation from the session that reads
  customer documents. A separate step, fed only structured fields, can create the ticket.
- **Detectors shrink the number, not to zero.** Even a 1% miss rate leaves about 20 compromised
  sessions a day here, and adaptive attackers push miss rates far higher than vendor test sets show.
  Architecture caps the impact; detection only reduces the frequency.

## Exercises

1. Add `fetch_url` to `inbox_summariser`. Why does a GET request count as communicating out?
2. Rerun with `--items 200` (a document-heavy agent). What happens to compromised sessions per day?
3. Redesign `inbox_assistant` so it can still draft replies. Where does the human approval go?
