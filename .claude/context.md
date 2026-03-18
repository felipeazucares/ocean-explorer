# Session Context

## Current Work
Phase 4 (Probe Domain Class) completed and merged to main this session.
Currently on branch `feature/phase-5-fastapi-routes`, ready to begin Phase 5.
CLAUDE.md updated to reflect Phase 4 complete, Phase 5 next.

## Recent Changes
- `app/domain/probe.py` — new Probe class with ExecuteResult dataclass
- `tests/unit/test_probe.py` — 23 unit tests for Probe (written before implementation)
- `CLAUDE.md` — progress tracker updated (Phase 4 done, Phase 5 next)

## Stable Features
- Phase 0: scaffolding, directory structure, conftest.py autouse fixture
- Phase 1: Pydantic models (DirectionEnum, CommandEnum, all request/response models)
- Phase 2: Direction class (`app/domain/direction.py`) — turn left/right, next_position
- Phase 3: Grid class (`app/domain/grid.py`) — is_valid, has_obstacle, boundary/obstacle block
- Phase 4: Probe class (`app/domain/probe.py`) — execute(), history, ExecuteResult
- All 89 unit tests passing

## Build
```bash
eval "$(pyenv init -)"
python -m pytest tests/unit/ -v
```

## Key Patterns
- Probe.execute() returns ExecuteResult(blocked_by, blocked_at); halts on first block
- Grid uses frozenset for obstacles; is_valid = in_bounds AND no obstacle
- conftest.py autouse fixture resets probe state before each test (module-level `probe = None` in main.py)
- Pre-commit hook blocks direct commits to main — always use feature branches

## Next Steps
1. Task 5.1: Write failing integration tests in `tests/integration/test_endpoints.py`
2. Task 5.2: Implement routes in `app/api/routes.py` (POST /probe/initialise, POST /probe/commands, GET /probe/history, GET /probe/state)
3. Task 5.3: Wire routes into `app/main.py` (FastAPI app, /health endpoint, logging middleware)
4. Task 5.4: Commit on `feature/phase-5-fastapi-routes`, merge to main, branch to `feature/phase-6-acceptance-tests`
