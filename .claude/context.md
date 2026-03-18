# Session Context

## Current Work
Phase 7 (Quality Gates) complete. Committed on feature/phase-7-quality-gates.
Merge to main is pending — user interrupted before the merge command was run.

## Recent Changes
- `app/main.py` — added HTTPException handler for ERROR-level logging of all HTTP errors
- `app/domain/probe.py` — removed unused `field` import (ruff fix)
- `tests/conftest.py` — removed unused `AsyncClient` import (ruff fix)
- `tests/integration/test_endpoints.py` — removed unused `pytest`, `TestClient`, `app` imports (ruff fix)
- `tests/unit/test_direction.py` — removed unused `pytest` import (ruff fix)
- `tests/unit/test_grid.py` — removed unused `pytest` import (ruff fix)
- `tests/unit/test_probe.py` — removed unused `pytest` import (ruff fix)
- `README.md` — corrected scenario/test count (49→50), coverage note (≥90%→100%), added constitution.md reference
- `CLAUDE.md` — updated progress tracker: Phase 7 complete, pending merge

## Stable Features
- 162 tests passing (89 unit + 23 integration + 50 acceptance)
- 100% code coverage across all app/ modules
- ruff check app/ tests/ — zero warnings
- All BDD scenarios covered 1:1 in tests/acceptance/test_scenarios.py
- API endpoints: POST /probe/initialise, POST /probe/commands, GET /probe/history, GET /probe/state, GET /health

## Build
```bash
python -m pytest --tb=short -q                        # run all 162 tests
python -m ruff check app/ tests/                      # linting (clean)
python -m pytest --cov=app --cov-report=term-missing  # coverage (100%)
uvicorn app.main:app --reload                         # start dev server
```

## Key Patterns
- Probe state: module-level `probe = None` in app/main.py, reset per test via conftest.py autouse fixture
- Circular import: routes.py imports `app.main` inside route functions (not at module level)
- HTTPException → ERROR log: custom handler in main.py logs all HTTP errors before returning JSON response
- Validation errors (422→400): RequestValidationError handler in main.py

## Next Steps
1. Run: `git checkout main && git merge feature/phase-7-quality-gates`
2. Verify: `git log --oneline -8` to confirm clean history
3. Optionally push to remote: `git push origin main`
4. Task 7.5 (Docker smoke test) could not be verified locally — Docker not installed on host
