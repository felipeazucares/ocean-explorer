# CLAUDE.md — Ocean Explorer Kata
# Version: 1.0.0

## Read First
Before doing anything else, read these documents in order:

1. constitution.md — non-negotiable principles. All articles apply.
2. spec.md — what the system does. Technology-agnostic.
3. bdd-scenarios.md — 50 acceptance scenarios. These define done.
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
Phase 7: Quality Gates — complete, merged to main

### Completed
- **Phase 7: Quality Gates** — committed on feature/phase-7-quality-gates
  - Task 7.1: HTTPException handler added to main.py — all HTTP errors now logged at ERROR level with method, path, status, and detail
  - Task 7.2: ruff check app/ tests/ — 8 unused imports removed (auto-fixed), zero warnings
  - Task 7.3: pytest --cov=app — 100% coverage across all modules (200 statements, 0 missed)
  - Task 7.4: README updated — corrected acceptance test count (49→50), coverage note (≥90%→100%), added constitution.md reference to design decisions section
  - Task 7.5: Smoke test via uvicorn — /health, /probe/initialise, /probe/commands all verified manually
  - Total tests passing: 162 (89 unit + 23 integration + 50 acceptance) — unchanged
- **Phase 6: Acceptance Tests** — merged to main
  - Task 6.1: 50 acceptance tests in tests/acceptance/test_scenarios.py — one per BDD scenario in bdd-scenarios.md, end-to-end via TestClient, no domain mocking
  - Task 6.2: Committed on feature/phase-6-acceptance-tests, merged to main
  - Total tests passing: 162 (89 unit + 23 integration + 50 acceptance)
- **Phase 5: FastAPI Routes** — merged to main
  - Task 5.1: 23 integration tests (POST /probe/initialise, POST /probe/commands, GET /probe/history, GET /probe/state — all status codes and response shapes)
  - Task 5.2: Routes in app/api/routes.py (_validate_initialise helper, 4 route handlers)
  - Task 5.3: app/main.py wired with router, /health endpoint, HTTP logging middleware, RequestValidationError handler (422 → 400)
  - Task 5.4: Committed on feature/phase-5-fastapi-routes, merged to main
  - Total tests passing: 112 (89 unit + 23 integration)
- **Phase 4: Probe Domain Class** — merged to main
  - Task 4.1: 23 unit tests (initialisation, forward/backward movement, turns, visit history, boundary blocking, obstacle blocking, execute sequence)
  - Task 4.2: Probe class in app/domain/probe.py with ExecuteResult dataclass
  - Task 4.3: Committed on feature/phase-4-probe-class, merged to main
- **Phase 3: Grid Domain Class** — merged to main
  - Task 3.1: 16 unit tests (is_valid, has_obstacle, is_boundary_block, is_obstacle_block)
  - Task 3.2: Grid class in app/domain/grid.py
  - Task 3.3: Committed on feature/phase-3-grid-class, merged to main
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

- None — all phases complete and merged to main.

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
- **Circular import avoidance**: routes.py imports `app.main` inside route functions (not at module level) to avoid circular dependency
- **Validation errors → 400**: RequestValidationError handler in main.py converts FastAPI's default 422 to 400 per spec requirement
- **.gitignore**: Added for Python artifacts (not in tasks.md but appropriate)
