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

---

## Progress Tracker

### Current Phase
Phase 3: Grid Domain Class — in progress

### Completed
- **Phase 2: Direction Domain Class** — merged to main
  - Task 2.1: 18 unit tests (turn_right, turn_left, full rotations, next_position F/B all 4 directions)
  - Task 2.2: Direction class in app/domain/direction.py
  - Task 2.3: Committed on feature/phase-2-direction-class, merged to main
- **Phase 1: Pydantic Models** — merged to main
  - Task 1.1: DirectionEnum (N/S/E/W)
  - Task 1.2: CommandEnum (F/B/L/R)
  - Task 1.3: InitialiseRequest, CommandRequest
  - Task 1.4: Position, ProbeState, CommandResponse, HistoryResponse, StateResponse, ErrorResponse
  - Task 1.5: Committed on feature/phase-1-pydantic-models, merged to main
- **Phase 0: Project Scaffolding** — merged to main
  - Task 0.0: Git initialisation (main + feature branch)
  - Task 0.1: Directory structure created and verified against spec
  - Task 0.1.1: conftest.py with autouse fixture for probe state isolation
  - Task 0.2: requirements.txt with all Article 1 dependencies
  - Task 0.3: Dockerfile and docker-compose.yml
  - Task 0.4: Committed on feature/phase-0-scaffolding, merged to main

### Pending
- Phase 3: Grid Domain Class
- Phase 4: Probe Domain Class
- Phase 5: FastAPI Routes
- Phase 6: Acceptance Tests
- Phase 7: Quality Gates

### Blockers
- None currently

### Git Hook Setup
After cloning, activate the pre-commit hook that blocks direct commits to main:
```
git config core.hooksPath git-hooks
```
Hook is in `git-hooks/pre-commit` and is version-controlled.

### Decisions Made
- **Remote**: origin set to https://github.com/felipeazucares/ocean-explorer.git
- **Python**: 3.12.13 via pyenv, set in .python-version
- **Docker**: Cannot verify locally (Docker not installed on host), but Dockerfile and docker-compose.yml are ready
- **Probe state**: Held as a module-level variable in app/main.py (`probe = None`), reset via conftest.py autouse fixture
- **.gitignore**: Added for Python artifacts (not in tasks.md but appropriate)
