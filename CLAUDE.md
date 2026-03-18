# CLAUDE.md — Ocean Explorer Kata
# Version: 1.0.0

## Read First
Before doing anything else, read these documents in order:

1. constitution.md — non-negotiable principles. All articles apply.
2. spec.md — what the system does. Technology-agnostic.
3. bdd-scenarios.md — 49 acceptance scenarios. These define done.
4. tasks.md — ordered build sequence. Follow phases strictly.

The documents form a dependency chain described in constitution.md
Article 12. If they conflict, constitution.md wins.

## Session Protocol
Each Claude Code session covers exactly one phase from tasks.md.

At the start of each session:
- Confirm which phase you are beginning
- Confirm all documents have been read
- Confirm the previous phase's tests are passing before starting

At the end of each session:
- All tests for the current phase must pass
- Commit and merge to main as described in tasks.md
- Report which phase is complete and what the next phase is

## Non-Negotiable Rules
- Write tests before implementation. Always. No exceptions.
- Never commit directly to main.
- Never add dependencies not listed in constitution.md Article 1.
- Never implement grid wrapping behaviour.
- Never generate a function longer than 20 lines.
- Flag ambiguity rather than assuming — stop and report.
- Never proceed to the next phase with failing tests.
