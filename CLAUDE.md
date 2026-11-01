# Working on this repository

This repo is the AI System Design Primer. Before writing or reviewing any section:

1. Read [STYLE.md](STYLE.md): audience, voice, length budgets, and the multi-provider research method
   (Anthropic, OpenAI, Google, AWS, Microsoft, plus primary literature and standards).
2. Read [ROADMAP.md](ROADMAP.md) for the forward backlog and [PLAN.md](PLAN.md) for the definition of done and verification debt. `primer.py readme` also regenerates the tables in 5.2 and 5.3 from the deep dives and front matter; edit those sources, not the generated blocks.
3. Each topic is two files (ADR 0007): a short primer page from [templates/section.md](templates/section.md)
   and a deep dive from [templates/deep-dive.md](templates/deep-dive.md) in `docs/deep-dives/`.
   Research into the deep dive first, then write the primer as its summary. Part 4 uses
   [templates/solved-design.md](templates/solved-design.md).
4. After editing, run:
   ```sh
   python3 scripts/primer.py check
   python3 scripts/primer.py readme
   python3 scripts/primer.py flashcards
   ```
5. Record unverified claims in PLAN.md rather than stating them confidently.
