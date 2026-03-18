# Session Context

## Current Work
Phase 5 (FastAPI Routes) completed and merged to main. CLAUDE.md updated.
Next session begins Phase 6: Acceptance Tests — 50 BDD scenarios from bdd-scenarios.md.

## Recent Changes
- `app/api/routes.py` — 4 route handlers: POST /probe/initialise, POST /probe/commands, GET /probe/history, GET /probe/state
- `app/main.py` — router wired in, /health endpoint, HTTP logging middleware, RequestValidationError handler (422 → 400)
- `tests/integration/test_endpoints.py` — 23 integration tests (all passing)
- `CLAUDE.md` — progress tracker updated: Phase 5 done, Phase 6 next

## Stable Features
- All 112 tests passing: 89 unit + 23 integration
- Domain layer (Direction, Grid, Probe) fully tested and independent of FastAPI
- Pydantic models in app/models.py cover all request/response shapes
- conftest.py autouse fixture resets `app.main.probe = None` before each test

## Build
```bash
python -m pytest tests/unit/ tests/integration/ -q   # 112 tests
python -m pytest tests/ -q                            # all tests
```

## Key Patterns
- `app.main.probe` is the in-memory probe singleton; imported inside route functions to avoid circular imports
- Blocked commands return HTTP 409 with full CommandResponse body (not just detail string) — use JSONResponse
- RequestValidationError → 400 handler lives in main.py (FastAPI default is 422)
- Branch naming: `feature/phase-N-description`; pre-commit hook blocks direct commits to main

## Next Steps
1. Create branch: `git checkout -b feature/phase-6-acceptance-tests`
2. Task 6.1: Implement `tests/acceptance/test_scenarios.py` — 50 named tests mapping every BDD scenario in bdd-scenarios.md
3. All 50 must pass before merging
4. Merge to main; then start Phase 7 (Quality Gates)
