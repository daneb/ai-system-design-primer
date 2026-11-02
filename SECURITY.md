# Security policy

This repository is a learning resource: Markdown pages, small lab scripts and diagram sources. It runs
no service, but two kinds of problem still matter.

## Report privately

- **A vulnerability in the scripts or CI**, such as a lab or `scripts/` file that could run untrusted
  input or leak a secret in CI.
- **Guidance that would make a reader's system less safe**, such as a control described wrongly, or a
  pattern recommended without the risk that makes it dangerous. These are as serious as code bugs,
  because people copy designs from this repository.

Use GitHub's private vulnerability reporting: the **Security** tab, then **Report a vulnerability**.
Please don't open a public issue for these. You should hear back within 14 days.

## Report in public

Factual errors, outdated figures, broken links and unclear explanations are welcome as ordinary
issues. Use the "Correction" issue template.

## Supported versions

Only the current `main` branch is maintained.
