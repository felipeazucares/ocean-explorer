# spec.md — Ocean Explorer Kata
# Version: 1.3.0

## Overview
A surface team is exploring the ocean floor using a remotely controlled
submersible probe. This system provides an API that enables the surface
team to initialise, command and query the probe. The probe navigates a
bounded grid representing the ocean floor.

This document defines WHAT the system does. It is technology-agnostic.
All technical decisions are in tasks.md.

---

## Interaction Model

The surface operator interacts with the probe through three sequential
steps. These steps define the expected workflow for every session.

### Step 1 — Initialise
The operator establishes the mission parameters before any movement
begins. This means providing:

- The grid dimensions (width and height)
- The probe's starting position as an x/y coordinate
- The direction the probe is facing (N, S, E, W)
- Optionally, a set of known obstacle coordinates on the grid

Example initialisation vector:
- Grid: 10 wide, 10 high
- Start: x=0, y=0, facing North
- Obstacles: (3,4), (5,5)

A successful initialisation resets all previous probe state including
visit history. The probe is now ready to receive commands.

### Step 2 — Send Commands
The operator sends a sequence of movement commands in a single request.
Commands are interpreted as a string of characters:

- F — move forward one cell in the current direction
- B — move backward one cell
- L — turn left 90 degrees (position unchanged)
- R — turn right 90 degrees (position unchanged)

Commands are executed in sequence. Execution stops at the first block
(boundary or obstacle). The response always includes the probe's
current position and direction.

Example command sequence: "F F R F F L F"

### Step 3 — Query
At any point the operator can:
- Query current probe state (position and direction)
- Retrieve the full visit history as an ordered list of coordinates

The history records every position the probe has occupied, including
the starting position and any revisits. It does not record turns.

---

## User Stories

### US-01: Initialise the Probe
As a surface operator,
I want to place the probe at a starting position and direction on the grid,
So that I can begin navigating the ocean floor from a known state.

Acceptance criteria:
- I can specify an x/y coordinate and a compass direction (N, S, E, W)
- I can specify the dimensions of the grid
- If the starting position is outside the grid, the system rejects it
- If a direction is invalid, the system rejects it
- A successful initialisation resets any previous probe state

---

### US-02: Send Movement Commands
As a surface operator,
I want to send a sequence of movement commands to the probe,
So that I can navigate it across the ocean floor.

Acceptance criteria:
- I can send one or more commands in a single request
- Valid commands are: F (forward), B (backward), L (turn left), R (turn right)
- The probe executes commands in sequence
- If an invalid command is included, the entire sequence is rejected before execution
- The response confirms the probe's final position and direction

---

### US-03: Boundary Protection
As a surface operator,
I want the probe to stop at the edge of the grid rather than fall off,
So that I do not lose the probe.

Acceptance criteria:
- If a movement would take the probe off the grid, it stops at its current position
- The response indicates the probe was blocked by a boundary
- Subsequent valid commands in the sequence are not executed after a boundary block
- The probe's position is always returned even when blocked

---

### US-04: Obstacle Avoidance
As a surface operator,
I want the probe to stop when it encounters an obstacle,
So that I do not damage the probe or the obstacle.

Acceptance criteria:
- The grid can be initialised with a set of obstacle coordinates
- If a movement would move the probe into an obstacle, it stops at its last valid position
- The response indicates the probe was blocked by an obstacle
- The obstacle's position is reported in the response
- Subsequent commands in the sequence are not executed after an obstacle block

---

### US-05: Visit History
As a surface operator,
I want to retrieve a summary of all coordinates the probe has visited,
So that I can review the coverage of the ocean floor exploration.

Acceptance criteria:
- The system records every position the probe occupies, including the start position
- I can request the full visit history at any time
- The history is returned as an ordered list of coordinates
- The history persists across multiple command requests within a session
- Reinitialising the probe resets the history

---

## System Constraints
- The ocean floor is a finite rectangular grid
- The probe occupies exactly one cell at any time
- The probe has exactly one direction at any time
- Commands are discrete — each command moves or turns exactly one step/unit
- The probe cannot occupy the same cell as an obstacle
- The probe cannot move outside the grid boundary

---

## Non-Functional Requirements

### Performance
- API must respond within 200ms for any command sequence of up to
  1000 commands on the default 10x10 grid
- FastAPI on uvicorn provides sufficient async I/O performance for
  this use case without additional optimisation

### Reliability
- All endpoints must return meaningful error responses with
  appropriate HTTP status codes — no unhandled exceptions exposed
  to the client
- Input validation failures must be reported with sufficient detail
  for the caller to correct their request

### Logging
- All requests and responses must be logged at INFO level
- Errors must be logged at ERROR level with sufficient context
  to diagnose the failure

### Concurrency — Known Constraint
Probe state is held in memory as a single application-level instance.
This is intentional for this kata submission.

Known implications:
- A single uvicorn worker processes one request at a time per event
  loop — concurrent access from a single client is safe in practice
- Multiple uvicorn workers (e.g. via gunicorn) would each hold
  independent probe state — two clients would see different probes
- Application instance scaling would have the same problem

A production implementation would require an external state store
(Redis or a database) to support multiple workers or application instance
scaling. This is a documented constraint, not an oversight.

### Scalability
- The current design supports a single probe per server instance
- The domain layer is intentionally decoupled from FastAPI to
  support future extension to multiple probes, persistent state,
  or alternative transport layers without rewriting business logic

---

## Out of Scope (this version)
- Multiple simultaneous probes
- Persistent storage across server restarts
- Authentication or authorisation
- 3D navigation (depth)
- Diagonal movement
- Grid wrapping

---

## Changelog

### Version 1.3.0
- Added changelog section
- Clarified "horizontal scaling" → "application instance scaling"

### Version 1.2.0
- Added Interaction Model section (Steps 1–3)
- Added Quick Start JSON examples to README

### Version 1.1.0
- Initial spec
