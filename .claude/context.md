# Session Context

## Current Work
Building the Ocean Explorer kata — a FastAPI submersible probe navigation API.
Phase 1 (Pydantic Models) completed and merged to main this session.
Phase 2 (Direction Domain Class) is next; branch `feature/phase-2-direction-class` already created.

## Recent Changes
- `app/models.py` — all enums and Pydantic models (DirectionEnum, CommandEnum, Position, InitialiseRequest, CommandRequest, ProbeState, CommandResponse, HistoryResponse, StateResponse, ErrorResponse)
- `tests/unit/test_models.py` — 32 unit tests for all models, all passing

## Stable Features
- Phase 0 scaffolding: full directory structure, conftest.py autouse fixture, requirements.txt, Dockerfile
- Phase 1 models: enums and request/response models define the full API contract

## Build
```bash
eval "$(pyenv init -)"
python -m pytest tests/unit/test_models.py -q   # 32 passed
python -m pytest -q                              # all tests
```

## Key Patterns
- pyenv shims need `eval "$(pyenv init -)"` in every Bash session
- Probe state is a module-level variable in `app/main.py`; conftest.py autouse fixture resets it between tests
- TDD: tests written before implementation — red first, then green
- No commits directly to main; branch per phase: `feature/phase-N-description`

## Next Steps
1. Write failing tests in `tests/unit/test_direction.py` (Task 2.1)
2. Implement `app/domain/direction.py` (Task 2.2) — turn left/right, next_position forward/backward
3. Run tests — all must pass
4. Commit: `feat: Direction class — Phase 2`
5. Merge to main, create `feature/phase-3-grid-class`
