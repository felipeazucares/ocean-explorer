# Ocean Explorer Kata
# Version: 1.4.0
## D12 Principal Engineer — Pre-Work Submission

## Running the API

### With Docker (recommended)
```
docker compose up
```
API available at http://localhost:8000
Interactive docs at http://localhost:8000/docs

To stop:
```
docker compose down
```

### Without Docker
The following commands create and activate a virtual environment, install dependencies, and start the server:
```
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API available at http://localhost:8000

To stop the server: `Ctrl+C`

To deactivate the virtual environment when done:
```
deactivate
```

---

## Interacting with the API

Once running, browse to http://localhost:8000/docs for the interactive
Swagger UI. The typical session follows three steps:

### 1. Initialise the Probe
POST to `/probe/initialise` with your mission parameters:

```json
{
  "x": 0,
  "y": 0,
  "direction": "N",
  "grid_width": 10,
  "grid_height": 10,
  "obstacles": [
    {"x": 3, "y": 4},
    {"x": 5, "y": 5}
  ]
}
```

To initialise with no obstacles, pass an empty list:
```json
{
  "x": 0,
  "y": 0,
  "direction": "N",
  "grid_width": 10,
  "grid_height": 10,
  "obstacles": []
}
```

### 2. Send Commands
POST to `/probe/commands` with a sequence of F, B, L, R characters:

```json
{
  "commands": ["F", "F", "R", "F", "F", "L", "F"]
}
```

The response includes the probe's current position, direction, and
whether it was blocked:

```json
{
  "position": {"x": 2, "y": 2},
  "direction": "N",
  "blocked_by": null,
  "blocked_at": null,
  "visited": [
    {"x": 0, "y": 0},
    {"x": 0, "y": 1},
    {"x": 0, "y": 2},
    {"x": 1, "y": 2},
    {"x": 2, "y": 2},
    {"x": 2, "y": 1},
    {"x": 2, "y": 2}
  ]
}
```

### 3. Query State and History
- GET `/probe/state` — current position and direction
- GET `/probe/history` — full ordered visit history with current state

---

## Prerequisites

### With Docker (recommended)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) — bundles everything needed, no additional setup required

### Without Docker
- Python 3.12 — install via [python.org](https://www.python.org/downloads/) or `brew install python@3.12`
- pip — bundled with Python 3.12
- The non-Docker path uses a Python virtual environment (`.venv`) to isolate dependencies from your system Python. This is created automatically by the setup commands below.

---

## Git Hooks

A pre-commit hook prevents direct commits to `main`. After cloning, activate it with:

```
git config core.hooksPath git-hooks
```

The hook lives in `git-hooks/pre-commit` and is version-controlled.

---

## Running the Tests

### With Docker
```
docker compose run --rm app pytest
docker compose run --rm app pytest --cov=app --cov-report=term-missing
```

### Without Docker
```
pytest
pytest --cov=app --cov-report=term-missing
```

---

## API Endpoints

| Method | Endpoint           | Description                              |
|--------|--------------------|------------------------------------------|
| POST   | /probe/initialise  | Place probe at starting position         |
| POST   | /probe/commands    | Send command sequence (F, B, L, R)       |
| GET    | /probe/state       | Query current probe position and direction |
| GET    | /probe/history     | Retrieve visited coordinates and current state |
| GET    | /health            | Health check                             |
| GET    | /docs              | OpenAPI interactive documentation        |

Every endpoint response includes the probe's current position and
direction. No call leaves the reviewer without knowing where the probe
is. Probe state is also returned in every command response and can be
queried at any time via GET /probe/state.

### Possible Enhancement
A `GET /probe/visualise` endpoint returning an ASCII grid representation
would make the API more intuitive to demo:

```
. . . . . . . . . .
. . . . . . . . . .
. . . . . . . . . .
. . . . . . . . . .
. . . . . . . . . .
. . . . . . . . . .
. . . . . . . . . .
. ^ . . . . . . . .
. . . . . . . . . .
. . . . . . . . . .
```

Where `^` = North, `v` = South, `>` = East, `<` = West, `X` = obstacle.
This is a non-functional extension and is out of scope for this
submission but noted as a natural next iteration.

---

## System Architecture

The system is structured in three layers, each independently testable:

```
┌─────────────────────────────────┐
│         FastAPI Layer           │  HTTP request/response
│  routes.py — thin wrapper only  │  Pydantic validation at boundary
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│         Domain Layer            │  Pure Python, no FastAPI dependency
│  Direction / Grid / Probe       │  All business logic lives here
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│         Models Layer            │  Pydantic v2 schemas
│  models.py — contract           │  Shared by API and domain
└─────────────────────────────────┘
```

The domain layer has no knowledge of FastAPI. It can be imported and
tested entirely without starting a server. The API layer is a thin
wrapper that handles HTTP concerns only — validation, serialisation,
status codes.

---

## Approach

### Methodology: Spec-Driven Development
This solution was built using a spec-first approach before any code
was written. The SDD documents in this zip (constitution.md, spec.md,
bdd-scenarios.md, tasks.md) formed the contract handed to the AI
coding agent.

Reading list that informed this approach:
- Martin Fowler on SDD: https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
- Thoughtworks on SDD: https://www.thoughtworks.com/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices

### BDD + TDD
BDD scenarios (bdd-scenarios.md) defined done. TDD unit tests drove
each domain class. The acceptance tests map 1:1 to the BDD scenarios
— 50 scenarios, 50 named acceptance tests.

### Key Design Decisions (see constitution.md for full constraints)
- **Hard boundaries**: probe stops and reports, does not wrap. The
  ocean floor is a physical space with edges, not a torus.
- **Origin (0,0) bottom-left, North = y+1**. Researched against
  common rover kata conventions before coding began.
- **Default grid 10x10**, fully configurable at initialisation.
- **Domain independence**: Direction, Grid and Probe are pure Python
  classes. The API is a thin wrapper — the domain is testable without
  a server.
- **Pydantic v2** validates all input at the API boundary. Invalid
  commands fail fast with meaningful errors before any state changes.
- **PEP8 compliance** enforced via ruff across all app and test code.
- **Revisiting a coordinate records duplicates** in history — the
  history is a journey log, not a unique set.

### AI Usage and Personal Differentiation
AI was used for: boilerplate fixtures, domain class implementation
against spec, Docker configuration, test scaffolding.

Human decisions: all SDD documents, BDD scenario authorship and
verification (including coordinate arithmetic verification), boundary
behaviour choice and justification, Pydantic model design as contract,
constitution.md guardrails for the agent, all refactoring decisions.


---

## Project Structure

```
ocean-explorer/
├── constitution.md      ← non-negotiable principles and guardrails
├── spec.md              ← what the system does (technology-agnostic)
├── bdd-scenarios.md     ← 50 acceptance scenarios
├── tasks.md             ← ordered build sequence
├── README.md
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── app/
│   ├── main.py          ← FastAPI app entry point
│   ├── models.py        ← Pydantic request/response schemas
│   ├── domain/
│   │   ├── direction.py ← Direction class and rotation logic
│   │   ├── grid.py      ← Grid class with boundary and obstacle logic
│   │   └── probe.py     ← Probe class with movement and history
│   └── api/
│       └── routes.py    ← FastAPI route handlers
└── tests/
    ├── conftest.py      ← shared fixtures
    ├── unit/            ← isolated domain class tests
    ├── integration/     ← FastAPI endpoint tests via TestClient
    └── acceptance/      ← BDD scenario tests (50 named tests)
```

---

## Test Coverage

```
pytest --cov=app returns 100% coverage
50 acceptance tests map directly to bdd-scenarios.md
```
