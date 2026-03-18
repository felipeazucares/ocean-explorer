# tasks.md — Ocean Explorer Kata
# Version: 1.6.0

## Purpose
This document provides the ordered build sequence for the AI agent.
Each task must be completed and tests passed before the next begins.
Read constitution.md before starting. Do not deviate from the stack
or principles defined there.

---

## Pre-Implementation Gates (constitution.md compliance check)
Before writing any code, confirm:
- [ ] Stack: Python 3.12 / FastAPI / Pydantic v2 / pytest / Docker
- [ ] Test-first: tests will be written before every implementation
- [ ] Hard boundaries: no wrapping behaviour will be implemented
- [ ] Clean code: no function over 20 lines, no magic strings
- [ ] Domain logic is independent of FastAPI

---

## Phase 0: Project Scaffolding

### Task 0.0 — Git Initialisation
```
git init
git checkout -b main
git checkout -b feature/phase-0-scaffolding
```

### Task 0.1 — Directory Structure
Create the following structure. Do not create any implementation files yet.

```
ocean-explorer/
├── constitution.md
├── spec.md
├── bdd-scenarios.md
├── tasks.md
├── README.md
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── direction.py
│   │   ├── grid.py
│   │   └── probe.py
│   └── api/
│       ├── __init__.py
│       └── routes.py
└── tests/
    ├── conftest.py
    ├── unit/
    │   ├── __init__.py
    │   ├── test_direction.py
    │   ├── test_grid.py
    │   └── test_probe.py
    ├── integration/
    │   ├── __init__.py
    │   └── test_endpoints.py
    └── acceptance/
        ├── __init__.py
        └── test_scenarios.py
```

### Task 0.1.1 - Conftest.py ###
* Note that  the probe lives as a single in-memory instance on the server. In tests, each test hits the same TestClient instance, which shares that state. If test_obstacle_blocks_forward leaves the probe at (0,1) and the next test expects it at (0,0), it'll fail.
* Therefore before writing any tests add an autouse fixture in conftest.py that reinitialises the probe to a clean state before each test.

### Task 0.2 — Dependencies
Create requirements.txt with:
- fastapi
- uvicorn
- pydantic>=2.0
- pytest
- httpx
- pytest-cov
- ruff

### Task 0.3 — Docker Setup
Create Dockerfile and docker-compose.yml.
`docker compose up` must start the API on port 8000.
`docker compose run --rm app pytest` must run all tests.

### Task 0.4 — Merge Phase 0
```
git add .
git commit -m "feat: project scaffolding — Phase 0"
git checkout main
git merge feature/phase-0-scaffolding
git checkout -b feature/phase-1-pydantic-models
```

---

## Phase 1: Pydantic Models (models.py)
Write models first. These are the API contract.
No implementation code yet.

### Task 1.1 — Direction Enum
```python
class DirectionEnum(str, Enum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"
```

### Task 1.2 — Command Enum
```python
class CommandEnum(str, Enum):
    FORWARD = "F"
    BACKWARD = "B"
    LEFT = "L"
    RIGHT = "R"
```

### Task 1.3 — Request Models
- InitialiseRequest: x, y, direction, grid_width (default 10),
  grid_height (default 10), obstacles (default empty list)
- CommandRequest: commands (list of CommandEnum)

### Task 1.4 — Response Models
- Position: x, y
- ProbeState: position, direction
- CommandResponse: probe_state, blocked_by (Optional: "boundary" | "obstacle"),
  blocked_at (Optional Position), visited (list of Position)
- HistoryResponse: position, direction, visited (list of Position)
- StateResponse: position, direction
- ErrorResponse: detail (str)

### Task 1.5 — Merge Phase 1
```
git add .
git commit -m "feat: Pydantic models — Phase 1"
git checkout main
git merge feature/phase-1-pydantic-models
git checkout -b feature/phase-2-direction-class
```

---

## Phase 2: Direction Domain Class

### Task 2.1 — Write tests first (tests/unit/test_direction.py)
Write failing tests for:
- turn_right from each of N, S, E, W
- turn_left from each of N, S, E, W
- full clockwise rotation returns to start
- full anticlockwise rotation returns to start
- next_position facing N from (0,0) returns (0,1)
- next_position facing S from (0,0) returns (0,-1)
- next_position facing E from (0,0) returns (1,0)
- next_position facing W from (0,0) returns (-1,0)
- backward movement (inverse of forward for each direction)

### Task 2.2 — Implement Direction class (app/domain/direction.py)
Implement only enough to pass the tests above.
The class must encapsulate direction state and support:
- Turning left and right
- Calculating the next position for forward and backward movement
Choose method signatures that are clean and idiomatic. Behaviour is
defined by the tests — do not over-engineer.

Run tests. All must pass before proceeding.

### Task 2.3 — Merge Phase 2
```
git add .
git commit -m "feat: Direction class — Phase 2"
git checkout main
git merge feature/phase-2-direction-class
git checkout -b feature/phase-3-grid-class
```

---

## Phase 3: Grid Domain Class

### Task 3.1 — Write tests first (tests/unit/test_grid.py)
Write failing tests for:
- is_valid(0, 0) on 10x10 grid returns True
- is_valid(-1, 0) returns False
- is_valid(0, -1) returns False
- is_valid(10, 0) returns False (0-indexed, max is 9)
- is_valid(9, 9) on 10x10 grid returns True
- is_valid(5, 5) with obstacle at (5,5) returns False
- is_valid(5, 6) with obstacle at (5,5) returns True
- has_obstacle(5, 5) with obstacle at (5,5) returns True
- has_obstacle(5, 6) with obstacle at (5,5) returns False
- is_boundary_block and is_obstacle_block distinguish correctly

### Task 3.2 — Implement Grid class (app/domain/grid.py)
Implement only enough to pass the tests above.
The class must encapsulate grid dimensions and obstacle positions and support:
- Validating whether a coordinate is within bounds
- Checking whether a coordinate contains an obstacle
- Reporting why a move is blocked (boundary or obstacle)
Choose method signatures that are clean and idiomatic. Behaviour is
defined by the tests — do not over-engineer.

Run tests. All must pass before proceeding.

### Task 3.3 — Merge Phase 3
```
git add .
git commit -m "feat: Grid class — Phase 3"
git checkout main
git merge feature/phase-3-grid-class
git checkout -b feature/phase-4-probe-class
```

---

## Phase 4: Probe Domain Class

### Task 4.1 — Write tests first (tests/unit/test_probe.py)
Write failing tests for:
- probe initialises at correct position and direction
- probe records start position in history
- move forward updates position correctly
- move backward updates position correctly
- turn left updates direction only (position unchanged)
- turn right updates direction only (position unchanged)
- turns do not add to visit history
- moves add to visit history
- probe stops at boundary and reports reason
- probe stops at obstacle and reports obstacle position
- commands after block are not executed
- execute sequence F,F,R,F from (0,0,N) results in (1,2,E)
- history is cumulative across multiple execute calls
- history does not include blocked position

### Task 4.2 — Implement Probe class (app/domain/probe.py)
Implement only enough to pass the tests above.
The class must encapsulate probe state (position, direction, history) and support:
- Executing a sequence of commands
- Returning execution results including block reason and blocked position
- Exposing visit history
Choose method signatures that are clean and idiomatic. Behaviour is
defined by the tests — do not over-engineer.

Run tests. All must pass before proceeding.

### Task 4.3 — Merge Phase 4
```
git add .
git commit -m "feat: Probe class — Phase 4"
git checkout main
git merge feature/phase-4-probe-class
git checkout -b feature/phase-5-fastapi-routes
```

---

## Phase 5: FastAPI Routes

### Task 5.1 — Write integration tests first (tests/integration/test_endpoints.py)
Write failing tests for:
- POST /probe/initialise returns 200 with valid request
- POST /probe/initialise returns 400 for out-of-bounds position
- POST /probe/initialise returns 400 for negative coordinates
- POST /probe/initialise returns 400 for invalid direction
- POST /probe/initialise returns 400 for position on obstacle
- POST /probe/initialise returns 400 for zero-dimension grid
- POST /probe/initialise returns 400 for obstacle outside grid bounds
- POST /probe/commands returns 200 for valid command sequence
- POST /probe/commands returns 200 for empty command sequence
- POST /probe/commands returns 400 for invalid commands
- POST /probe/commands returns 400 if probe not initialised
- POST /probe/commands returns 409 when blocked by boundary
- POST /probe/commands returns 409 when blocked by obstacle
- GET /probe/history returns 200 with ordered visit list
- GET /probe/history returns 400 if probe not yet initialised
- GET /probe/state returns 200 with current position and direction
- GET /probe/state returns 400 if probe not yet initialised
- All responses conform to Pydantic response models

### Task 5.2 — Implement routes (app/api/routes.py)
- POST /probe/initialise
- POST /probe/commands
- GET /probe/history
- GET /probe/state

### Task 5.3 — Wire routes into main.py
- Create FastAPI app instance
- Include router
- Add /health endpoint returning 200
- Add request/response logging middleware at INFO level
- Add error logging at ERROR level with request context

Run integration tests. All must pass before proceeding.

### Task 5.4 — Merge Phase 5
```
git add .
git commit -m "feat: FastAPI routes — Phase 5"
git checkout main
git merge feature/phase-5-fastapi-routes
git checkout -b feature/phase-6-acceptance-tests
```

---

## Phase 6: Acceptance Tests

### Task 6.1 — Implement acceptance tests (tests/acceptance/test_scenarios.py)
Implement tests covering every scenario in bdd-scenarios.md.
These are end-to-end tests using TestClient.
Do not mock any domain classes here.

Map each BDD scenario to a named test function:
- test_successful_initialisation
- test_initialisation_at_non_zero_position
- test_initialisation_rejected_outside_grid
- test_initialisation_rejected_negative_x
- test_initialisation_rejected_negative_y
- test_initialisation_rejected_invalid_direction
- test_initialisation_rejected_zero_width_grid
- test_initialisation_rejected_zero_height_grid
- test_initialisation_rejected_obstacle_outside_grid
- test_reinitialisation_resets_state
- test_move_forward_north
- test_move_forward_south
- test_move_forward_east
- test_move_forward_west
- test_move_backward_north
- test_move_backward_south
- test_move_backward_east
- test_move_backward_west
- test_turn_left_from_north
- test_turn_right_from_north
- test_full_clockwise_rotation
- test_full_anticlockwise_rotation
- test_multi_command_sequence
- test_empty_command_sequence
- test_invalid_command_rejected
- test_blocked_north_boundary_forward
- test_blocked_south_boundary_forward
- test_blocked_east_boundary_forward
- test_blocked_west_boundary_forward
- test_commands_after_block_not_executed
- test_backward_blocked_south_boundary
- test_backward_blocked_north_boundary
- test_backward_blocked_west_boundary
- test_backward_blocked_east_boundary
- test_obstacle_blocks_forward
- test_obstacle_blocks_backward
- test_navigate_around_obstacle
- test_cannot_initialise_on_obstacle
- test_multiple_obstacles
- test_history_records_start
- test_history_records_moves
- test_turns_not_in_history
- test_history_persists_across_requests
- test_history_resets_on_reinitialise
- test_blocked_position_not_in_history
- test_revisiting_coordinate_recorded_each_time
- test_commands_before_initialisation_rejected
- test_history_before_initialisation_rejected
- test_probe_state_query
- test_health_endpoint

Run all tests. All 50 must pass before proceeding.

### Task 6.2 — Merge Phase 6
```
git add .
git commit -m "feat: acceptance tests — Phase 6"
git checkout main
git merge feature/phase-6-acceptance-tests
git checkout -b feature/phase-7-quality-gates
```

---

## Phase 7: Quality Gates

### Task 7.1 — Logging
Verify logging is in place per spec.md NFR:
- All requests and responses logged at INFO level
- Errors logged at ERROR level with sufficient diagnostic context
- Add a middleware or FastAPI event hook in main.py to handle request/response logging
- Confirm no sensitive data is logged
- Run tests to confirm logging does not break any existing behaviour

### Task 7.2 — PEP8 Linting
Run ruff to enforce PEP8 compliance. Zero warnings permitted.
```
ruff check app/
ruff check tests/
```
Fix any issues before proceeding. PEP8 compliance is non-negotiable
per constitution.md Article 7.

### Task 7.3 — Coverage
Run pytest --cov=app --cov-report=term-missing
Target: 90% coverage minimum.
Document any excluded lines with justification.

### Task 7.4 — README
Update the README.md covering:
- How to run: `docker compose up`
- How to run tests: `docker compose run --rm app pytest`
- API endpoints summary
- Key design decisions (reference constitution.md)
- Link to /docs for OpenAPI

### Task 7.5 — Smoke Test
Start the API via docker compose.
Manually verify /docs loads and all endpoints are visible.
Manually send one initialise and one command request.

---

## Definition of Done
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All 50 acceptance tests pass
- [ ] ruff linting passes with zero warnings
- [ ] Coverage >= 90%
- [ ] Docker compose up starts server cleanly
- [ ] /docs endpoint renders OpenAPI schema
- [ ] README complete
- [ ] constitution.md, spec.md, bdd-scenarios.md, tasks.md included in zip
- [ ] All feature branches merged to main
- [ ] No commits directly on main
- [ ] Git log tells the story of the build sequence

### Final merge
```
git add .
git commit -m "feat: quality gates and README — Phase 7"
git checkout main
git merge feature/phase-7-quality-gates
```

---

## Changelog

### Version 1.6.0
- Fixed duplicate Task 7.2 numbering — renumbered Phase 7 tasks sequentially (7.1–7.5)

### Version 1.5.0
- Loosened Tasks 2.2, 3.2, 4.2 — removed prescribed method signatures,
  replaced with behavioural intent. Tests remain the contract.

### Version 1.4.0
- Added logging middleware task to Task 5.3
- Added test_health_endpoint to acceptance test list
- Updated acceptance test count from 49 to 50
- Added this changelog

### Version 1.3.0
- Added Task 0.1.1 — conftest.py autouse fixture for test isolation
- Fixed typo: Configtest → Conftest

### Version 1.2.0
- Added conftest.py note on probe state isolation

### Version 1.1.0
- Initial build sequence
