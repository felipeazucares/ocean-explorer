# bdd-scenarios.md — Ocean Explorer Kata
# Version: 1.2.0

## Purpose
These scenarios define the acceptance criteria for the Ocean Explorer API.
Each scenario maps to a user story in spec.md.
All scenarios must pass before any feature is considered done.
These are the outermost test ring — they drive everything beneath them.

---

## Feature: Probe Initialisation (US-01)

### Scenario: Successful initialisation
Given a 10x10 grid with no obstacles
When I initialise the probe at (0, 0) facing North
Then the probe is at (0, 0)
And the probe is facing North
And the visit history contains only (0, 0)
And the response status is 200

### Scenario: Initialisation at non-zero position
Given a 10x10 grid with no obstacles
When I initialise the probe at (5, 7) facing East
Then the probe is at (5, 7)
And the probe is facing East
And the visit history contains only (5, 7)

### Scenario: Initialisation rejected when position is outside grid
Given a 10x10 grid with no obstacles
When I initialise the probe at (10, 10) facing North
Then the response status is 400
And the response contains an error message describing the invalid position

### Scenario: Initialisation rejected for negative x coordinate
Given a 10x10 grid with no obstacles
When I initialise the probe at (-1, 0) facing North
Then the response status is 400
And the response contains an error message describing the invalid position

### Scenario: Initialisation rejected for negative y coordinate
Given a 10x10 grid with no obstacles
When I initialise the probe at (0, -1) facing North
Then the response status is 400
And the response contains an error message describing the invalid position

### Scenario: Initialisation rejected for invalid direction
Given a 10x10 grid with no obstacles
When I initialise the probe at (0, 0) facing X
Then the response status is 400
And the response contains an error message describing the invalid direction

### Scenario: Initialisation rejected for zero-width grid
Given a grid with width 0 and height 10
When I initialise the probe at (0, 0) facing North
Then the response status is 400
And the response contains an error message describing the invalid grid dimensions

### Scenario: Initialisation rejected for zero-height grid
Given a grid with width 10 and height 0
When I initialise the probe at (0, 0) facing North
Then the response status is 400
And the response contains an error message describing the invalid grid dimensions

### Scenario: Initialisation rejected when obstacle is outside grid bounds
Given a 10x10 grid
When I initialise with an obstacle at (15, 15)
Then the response status is 400
And the response contains an error message describing the invalid obstacle position

### Scenario: Re-initialisation resets all state
Given a probe previously initialised at (3, 3) facing South with some visit history
When I initialise the probe at (1, 1) facing West
Then the probe is at (1, 1)
And the probe is facing West
And the visit history contains only (1, 1)

---

## Feature: Movement Commands (US-02)

### Scenario: Move forward facing North
Given a 10x10 grid with no obstacles
And the probe is at (0, 0) facing North
When I send command sequence "F"
Then the probe is at (0, 1)
And the probe is facing North
And the response status is 200

### Scenario: Move forward facing South
Given a 10x10 grid with no obstacles
And the probe is at (5, 5) facing South
When I send command sequence "F"
Then the probe is at (5, 4)
And the probe is facing South

### Scenario: Move forward facing East
Given a 10x10 grid with no obstacles
And the probe is at (5, 5) facing East
When I send command sequence "F"
Then the probe is at (6, 5)
And the probe is facing East

### Scenario: Move forward facing West
Given a 10x10 grid with no obstacles
And the probe is at (5, 5) facing West
When I send command sequence "F"
Then the probe is at (4, 5)
And the probe is facing West

### Scenario: Move backward facing North
Given a 10x10 grid with no obstacles
And the probe is at (5, 5) facing North
When I send command sequence "B"
Then the probe is at (5, 4)
And the probe is facing North

### Scenario: Move backward facing South
Given a 10x10 grid with no obstacles
And the probe is at (5, 5) facing South
When I send command sequence "B"
Then the probe is at (5, 6)
And the probe is facing South

### Scenario: Move backward facing East
Given a 10x10 grid with no obstacles
And the probe is at (5, 5) facing East
When I send command sequence "B"
Then the probe is at (4, 5)
And the probe is facing East

### Scenario: Move backward facing West
Given a 10x10 grid with no obstacles
And the probe is at (5, 5) facing West
When I send command sequence "B"
Then the probe is at (6, 5)
And the probe is facing West

### Scenario: Turn left from North
Given a 10x10 grid with no obstacles
And the probe is at (0, 0) facing North
When I send command sequence "L"
Then the probe is at (0, 0)
And the probe is facing West

### Scenario: Turn right from North
Given a 10x10 grid with no obstacles
And the probe is at (0, 0) facing North
When I send command sequence "R"
Then the probe is at (0, 0)
And the probe is facing East

### Scenario: Full clockwise rotation returns to original direction
Given a 10x10 grid with no obstacles
And the probe is at (0, 0) facing North
When I send command sequence "R R R R"
Then the probe is at (0, 0)
And the probe is facing North

### Scenario: Full anticlockwise rotation returns to original direction
Given a 10x10 grid with no obstacles
And the probe is at (0, 0) facing North
When I send command sequence "L L L L"
Then the probe is at (0, 0)
And the probe is facing North

### Scenario: Execute a multi-command sequence
Given a 10x10 grid with no obstacles
And the probe is at (0, 0) facing North
When I send command sequence "F F R F"
Then the probe is at (1, 2)
And the probe is facing East

### Scenario: Empty command sequence returns current state unchanged
Given a 10x10 grid with no obstacles
And the probe is at (3, 3) facing East
When I send an empty command sequence
Then the probe is at (3, 3)
And the probe is facing East
And the response status is 200

### Scenario: Invalid command in sequence is rejected
Given a 10x10 grid with no obstacles
And the probe is at (0, 0) facing North
When I send command sequence "F X F"
Then the response status is 400
And the probe remains at (0, 0)
And the response contains an error message describing the invalid command

---

## Feature: Boundary Protection (US-03)

### Scenario: Probe blocked at North boundary moving forward
Given a 10x10 grid with no obstacles
And the probe is at (0, 9) facing North
When I send command sequence "F"
Then the probe remains at (0, 9)
And the response status is 409
And the response indicates the probe was blocked by a boundary

### Scenario: Probe blocked at South boundary moving forward
Given a 10x10 grid with no obstacles
And the probe is at (0, 0) facing South
When I send command sequence "F"
Then the probe remains at (0, 0)
And the response status is 409
And the response indicates the probe was blocked by a boundary

### Scenario: Probe blocked at East boundary moving forward
Given a 10x10 grid with no obstacles
And the probe is at (9, 0) facing East
When I send command sequence "F"
Then the probe remains at (9, 0)
And the response status is 409
And the response indicates the probe was blocked by a boundary

### Scenario: Probe blocked at West boundary moving forward
Given a 10x10 grid with no obstacles
And the probe is at (0, 0) facing West
When I send command sequence "F"
Then the probe remains at (0, 0)
And the response status is 409
And the response indicates the probe was blocked by a boundary

### Scenario: Commands after boundary block are not executed
Given a 10x10 grid with no obstacles
And the probe is at (0, 9) facing North
When I send command sequence "F F F"
Then the probe remains at (0, 9)
And the response indicates the probe was blocked by a boundary

### Scenario: Backward move blocked at South boundary facing North
Given a 10x10 grid with no obstacles
And the probe is at (0, 0) facing North
When I send command sequence "B"
Then the probe remains at (0, 0)
And the response indicates the probe was blocked by a boundary

### Scenario: Backward move blocked at North boundary facing South
Given a 10x10 grid with no obstacles
And the probe is at (5, 9) facing South
When I send command sequence "B"
Then the probe remains at (5, 9)
And the response indicates the probe was blocked by a boundary

### Scenario: Backward move blocked at West boundary facing East
Given a 10x10 grid with no obstacles
And the probe is at (0, 5) facing East
When I send command sequence "B"
Then the probe remains at (0, 5)
And the response indicates the probe was blocked by a boundary

### Scenario: Backward move blocked at East boundary facing West
Given a 10x10 grid with no obstacles
And the probe is at (9, 5) facing West
When I send command sequence "B"
Then the probe remains at (9, 5)
And the response indicates the probe was blocked by a boundary

---

## Feature: Obstacle Avoidance (US-04)

### Scenario: Probe blocked by obstacle ahead when moving forward
Given a 10x10 grid with an obstacle at (0, 2)
And the probe is at (0, 0) facing North
When I send command sequence "F F F"
Then the probe is at (0, 1)
And the response status is 409
And the response indicates the probe was blocked by an obstacle
And the response identifies the obstacle position as (0, 2)

### Scenario: Probe blocked by obstacle when moving backward
Given a 10x10 grid with an obstacle at (0, 3)
And the probe is at (0, 5) facing North
When I send command sequence "B B B"
Then the probe is at (0, 4)
And the response status is 409
And the response indicates the probe was blocked by an obstacle
And the response identifies the obstacle position as (0, 3)

### Scenario: Probe navigates around an obstacle
Given a 10x10 grid with an obstacle at (0, 2)
And the probe is at (0, 0) facing North
When I send command sequence "F R F L F"
Then the probe is at (1, 2)
And the probe is facing North

### Scenario: Probe cannot be initialised on an obstacle
Given a 10x10 grid with an obstacle at (3, 3)
When I initialise the probe at (3, 3) facing North
Then the response status is 400
And the response contains an error message describing the obstacle conflict

### Scenario: Multiple obstacles on grid
Given a 10x10 grid with obstacles at (2, 2) and (4, 4)
And the probe is at (0, 0) facing North
When I send command sequence "F F R F F"
Then the probe is at (1, 2)
And the response indicates the probe was blocked by an obstacle

---

## Feature: Visit History (US-05)

### Scenario: History records start position
Given a 10x10 grid with no obstacles
When I initialise the probe at (0, 0) facing North
Then the visit history contains [(0, 0)]

### Scenario: History records each position visited
Given a 10x10 grid with no obstacles
And the probe is at (0, 0) facing North
When I send command sequence "F F R F"
Then the visit history contains [(0,0), (0,1), (0,2), (1,2)]

### Scenario: Turns do not add new entries to history
Given a 10x10 grid with no obstacles
And the probe is at (0, 0) facing North
When I send command sequence "R R"
Then the visit history contains [(0, 0)]

### Scenario: History persists across multiple command requests
Given a 10x10 grid with no obstacles
And the probe is at (0, 0) facing North
And I have previously sent command sequence "F F"
When I send command sequence "R F"
Then the visit history contains [(0,0), (0,1), (0,2), (1,2)]

### Scenario: History resets on re-initialisation
Given the probe has visited several positions
When I reinitialise the probe at (0, 0) facing North
Then the visit history contains only [(0, 0)]

### Scenario: Blocked position is not added to history
Given a 10x10 grid with an obstacle at (0, 2)
And the probe is at (0, 1) facing North
When I send command sequence "F"
Then the probe remains at (0, 1)
And the visit history does not contain (0, 2)

### Scenario: Revisiting a coordinate is recorded each time
Given a 10x10 grid with no obstacles
And the probe is at (0, 0) facing North
When I send command sequence "F B"
Then the visit history contains [(0,0), (0,1), (0,0)]
And the visit history has 3 entries

---

## Feature: API Session State (Global Edge Cases)

### Scenario: Commands sent before initialisation are rejected
Given the API has just started with no probe initialised
When I send command sequence "F F"
Then the response status is 400
And the response contains an error message indicating the probe is not initialised

### Scenario: History requested before initialisation is rejected
Given the API has just started with no probe initialised
When I request the visit history
Then the response status is 400
And the response contains an error message indicating the probe is not initialised

### Scenario: Probe state can be queried without sending commands
Given a 10x10 grid with no obstacles
And the probe is at (3, 4) facing West
When I request the current probe state
Then the probe is at (3, 4)
And the probe is facing West
And the response status is 200

### Scenario: Health endpoint returns 200
Given the API is running
When I request GET /health
Then the response status is 200

---

## Changelog

### Version 1.2.0
- Added health endpoint scenario (Global)
- Moved changelog from header to end of document

### Version 1.1.0
- Added negative coordinate rejection (Initialisation)
- Added zero-dimension grid rejection (Initialisation)
- Added obstacle outside grid bounds rejection (Initialisation)
- Added forward movement coverage for S, E, W directions (Movement)
- Added backward movement coverage for S, E, W directions (Movement)
- Added empty command sequence scenario (Movement)
- Added anticlockwise full rotation (Movement)
- Added backward movement into obstacle (Obstacle Avoidance)
- Added backward boundary coverage for all four directions (Boundary)
- Added duplicate coordinate history behaviour (History)
- Added commands sent before initialisation (Global)
- Added history requested before initialisation (Global)
- Added probe state query endpoint scenario (Global)

### Version 1.0.0
- Initial scenarios
