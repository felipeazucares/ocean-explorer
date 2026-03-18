"""Acceptance tests for Ocean Explorer — Phase 6.

Each test maps 1-to-1 to a named scenario in bdd-scenarios.md.
Tests use TestClient end-to-end with no domain mocking.
"""

INIT_URL = "/probe/initialise"
CMD_URL = "/probe/commands"
HISTORY_URL = "/probe/history"
STATE_URL = "/probe/state"
HEALTH_URL = "/health"

BASE = {"x": 0, "y": 0, "direction": "N", "grid_width": 10, "grid_height": 10}


def _init(client, **kw):
    """POST /probe/initialise with BASE merged with kw."""
    return client.post(INIT_URL, json={**BASE, **kw})


def _cmd(client, seq: str):
    """POST /probe/commands from a space-separated command string."""
    cmds = seq.split() if seq.strip() else []
    return client.post(CMD_URL, json={"commands": cmds})


# ---------------------------------------------------------------------------
# Feature: Probe Initialisation (US-01)
# ---------------------------------------------------------------------------


def test_successful_initialisation(client):
    """Scenario: Successful initialisation."""
    resp = _init(client)
    assert resp.status_code == 200
    body = resp.json()
    assert body["position"] == {"x": 0, "y": 0}
    assert body["direction"] == "N"
    hist = client.get(HISTORY_URL).json()
    assert hist["visited"] == [{"x": 0, "y": 0}]


def test_initialisation_at_non_zero_position(client):
    """Scenario: Initialisation at non-zero position."""
    resp = _init(client, x=5, y=7, direction="E")
    assert resp.status_code == 200
    body = resp.json()
    assert body["position"] == {"x": 5, "y": 7}
    assert body["direction"] == "E"
    hist = client.get(HISTORY_URL).json()
    assert hist["visited"] == [{"x": 5, "y": 7}]


def test_initialisation_rejected_outside_grid(client):
    """Scenario: Initialisation rejected when position is outside grid."""
    resp = _init(client, x=10, y=10)
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_initialisation_rejected_negative_x(client):
    """Scenario: Initialisation rejected for negative x coordinate."""
    resp = _init(client, x=-1, y=0)
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_initialisation_rejected_negative_y(client):
    """Scenario: Initialisation rejected for negative y coordinate."""
    resp = _init(client, x=0, y=-1)
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_initialisation_rejected_invalid_direction(client):
    """Scenario: Initialisation rejected for invalid direction."""
    resp = client.post(INIT_URL, json={**BASE, "direction": "X"})
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_initialisation_rejected_zero_width_grid(client):
    """Scenario: Initialisation rejected for zero-width grid."""
    resp = _init(client, grid_width=0)
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_initialisation_rejected_zero_height_grid(client):
    """Scenario: Initialisation rejected for zero-height grid."""
    resp = _init(client, grid_height=0)
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_initialisation_rejected_obstacle_outside_grid(client):
    """Scenario: Initialisation rejected when obstacle is outside grid bounds."""
    resp = _init(client, obstacles=[{"x": 15, "y": 15}])
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_reinitialisation_resets_state(client):
    """Scenario: Re-initialisation resets all state."""
    _init(client, x=3, y=3, direction="S")
    _cmd(client, "F F")
    resp = _init(client, x=1, y=1, direction="W")
    assert resp.status_code == 200
    body = resp.json()
    assert body["position"] == {"x": 1, "y": 1}
    assert body["direction"] == "W"
    hist = client.get(HISTORY_URL).json()
    assert hist["visited"] == [{"x": 1, "y": 1}]


# ---------------------------------------------------------------------------
# Feature: Movement Commands (US-02)
# ---------------------------------------------------------------------------


def test_move_forward_north(client):
    """Scenario: Move forward facing North."""
    _init(client, x=0, y=0, direction="N")
    resp = _cmd(client, "F")
    assert resp.status_code == 200
    state = resp.json()["probe_state"]
    assert state["position"] == {"x": 0, "y": 1}
    assert state["direction"] == "N"


def test_move_forward_south(client):
    """Scenario: Move forward facing South."""
    _init(client, x=5, y=5, direction="S")
    resp = _cmd(client, "F")
    assert resp.status_code == 200
    state = resp.json()["probe_state"]
    assert state["position"] == {"x": 5, "y": 4}
    assert state["direction"] == "S"


def test_move_forward_east(client):
    """Scenario: Move forward facing East."""
    _init(client, x=5, y=5, direction="E")
    resp = _cmd(client, "F")
    assert resp.status_code == 200
    state = resp.json()["probe_state"]
    assert state["position"] == {"x": 6, "y": 5}
    assert state["direction"] == "E"


def test_move_forward_west(client):
    """Scenario: Move forward facing West."""
    _init(client, x=5, y=5, direction="W")
    resp = _cmd(client, "F")
    assert resp.status_code == 200
    state = resp.json()["probe_state"]
    assert state["position"] == {"x": 4, "y": 5}
    assert state["direction"] == "W"


def test_move_backward_north(client):
    """Scenario: Move backward facing North."""
    _init(client, x=5, y=5, direction="N")
    resp = _cmd(client, "B")
    assert resp.status_code == 200
    state = resp.json()["probe_state"]
    assert state["position"] == {"x": 5, "y": 4}
    assert state["direction"] == "N"


def test_move_backward_south(client):
    """Scenario: Move backward facing South."""
    _init(client, x=5, y=5, direction="S")
    resp = _cmd(client, "B")
    assert resp.status_code == 200
    state = resp.json()["probe_state"]
    assert state["position"] == {"x": 5, "y": 6}
    assert state["direction"] == "S"


def test_move_backward_east(client):
    """Scenario: Move backward facing East."""
    _init(client, x=5, y=5, direction="E")
    resp = _cmd(client, "B")
    assert resp.status_code == 200
    state = resp.json()["probe_state"]
    assert state["position"] == {"x": 4, "y": 5}
    assert state["direction"] == "E"


def test_move_backward_west(client):
    """Scenario: Move backward facing West."""
    _init(client, x=5, y=5, direction="W")
    resp = _cmd(client, "B")
    assert resp.status_code == 200
    state = resp.json()["probe_state"]
    assert state["position"] == {"x": 6, "y": 5}
    assert state["direction"] == "W"


def test_turn_left_from_north(client):
    """Scenario: Turn left from North."""
    _init(client, x=0, y=0, direction="N")
    resp = _cmd(client, "L")
    assert resp.status_code == 200
    state = resp.json()["probe_state"]
    assert state["position"] == {"x": 0, "y": 0}
    assert state["direction"] == "W"


def test_turn_right_from_north(client):
    """Scenario: Turn right from North."""
    _init(client, x=0, y=0, direction="N")
    resp = _cmd(client, "R")
    assert resp.status_code == 200
    state = resp.json()["probe_state"]
    assert state["position"] == {"x": 0, "y": 0}
    assert state["direction"] == "E"


def test_full_clockwise_rotation(client):
    """Scenario: Full clockwise rotation returns to original direction."""
    _init(client, x=0, y=0, direction="N")
    resp = _cmd(client, "R R R R")
    assert resp.status_code == 200
    state = resp.json()["probe_state"]
    assert state["position"] == {"x": 0, "y": 0}
    assert state["direction"] == "N"


def test_full_anticlockwise_rotation(client):
    """Scenario: Full anticlockwise rotation returns to original direction."""
    _init(client, x=0, y=0, direction="N")
    resp = _cmd(client, "L L L L")
    assert resp.status_code == 200
    state = resp.json()["probe_state"]
    assert state["position"] == {"x": 0, "y": 0}
    assert state["direction"] == "N"


def test_multi_command_sequence(client):
    """Scenario: Execute a multi-command sequence."""
    _init(client, x=0, y=0, direction="N")
    resp = _cmd(client, "F F R F")
    assert resp.status_code == 200
    state = resp.json()["probe_state"]
    assert state["position"] == {"x": 1, "y": 2}
    assert state["direction"] == "E"


def test_empty_command_sequence(client):
    """Scenario: Empty command sequence returns current state unchanged."""
    _init(client, x=3, y=3, direction="E")
    resp = client.post(CMD_URL, json={"commands": []})
    assert resp.status_code == 200
    state = resp.json()["probe_state"]
    assert state["position"] == {"x": 3, "y": 3}
    assert state["direction"] == "E"


def test_invalid_command_rejected(client):
    """Scenario: Invalid command in sequence is rejected."""
    _init(client, x=0, y=0, direction="N")
    resp = client.post(CMD_URL, json={"commands": ["F", "X", "F"]})
    assert resp.status_code == 400
    assert "detail" in resp.json()
    state = client.get(STATE_URL).json()
    assert state["position"] == {"x": 0, "y": 0}


# ---------------------------------------------------------------------------
# Feature: Boundary Protection (US-03)
# ---------------------------------------------------------------------------


def test_blocked_north_boundary_forward(client):
    """Scenario: Probe blocked at North boundary moving forward."""
    _init(client, x=0, y=9, direction="N")
    resp = _cmd(client, "F")
    assert resp.status_code == 409
    body = resp.json()
    assert body["blocked_by"] == "boundary"
    assert body["probe_state"]["position"] == {"x": 0, "y": 9}


def test_blocked_south_boundary_forward(client):
    """Scenario: Probe blocked at South boundary moving forward."""
    _init(client, x=0, y=0, direction="S")
    resp = _cmd(client, "F")
    assert resp.status_code == 409
    body = resp.json()
    assert body["blocked_by"] == "boundary"
    assert body["probe_state"]["position"] == {"x": 0, "y": 0}


def test_blocked_east_boundary_forward(client):
    """Scenario: Probe blocked at East boundary moving forward."""
    _init(client, x=9, y=0, direction="E")
    resp = _cmd(client, "F")
    assert resp.status_code == 409
    body = resp.json()
    assert body["blocked_by"] == "boundary"
    assert body["probe_state"]["position"] == {"x": 9, "y": 0}


def test_blocked_west_boundary_forward(client):
    """Scenario: Probe blocked at West boundary moving forward."""
    _init(client, x=0, y=0, direction="W")
    resp = _cmd(client, "F")
    assert resp.status_code == 409
    body = resp.json()
    assert body["blocked_by"] == "boundary"
    assert body["probe_state"]["position"] == {"x": 0, "y": 0}


def test_commands_after_block_not_executed(client):
    """Scenario: Commands after boundary block are not executed."""
    _init(client, x=0, y=9, direction="N")
    resp = _cmd(client, "F F F")
    assert resp.status_code == 409
    body = resp.json()
    assert body["blocked_by"] == "boundary"
    assert body["probe_state"]["position"] == {"x": 0, "y": 9}


def test_backward_blocked_south_boundary(client):
    """Scenario: Backward move blocked at South boundary facing North."""
    _init(client, x=0, y=0, direction="N")
    resp = _cmd(client, "B")
    assert resp.status_code == 409
    assert resp.json()["blocked_by"] == "boundary"
    assert resp.json()["probe_state"]["position"] == {"x": 0, "y": 0}


def test_backward_blocked_north_boundary(client):
    """Scenario: Backward move blocked at North boundary facing South."""
    _init(client, x=5, y=9, direction="S")
    resp = _cmd(client, "B")
    assert resp.status_code == 409
    assert resp.json()["blocked_by"] == "boundary"
    assert resp.json()["probe_state"]["position"] == {"x": 5, "y": 9}


def test_backward_blocked_west_boundary(client):
    """Scenario: Backward move blocked at West boundary facing East."""
    _init(client, x=0, y=5, direction="E")
    resp = _cmd(client, "B")
    assert resp.status_code == 409
    assert resp.json()["blocked_by"] == "boundary"
    assert resp.json()["probe_state"]["position"] == {"x": 0, "y": 5}


def test_backward_blocked_east_boundary(client):
    """Scenario: Backward move blocked at East boundary facing West."""
    _init(client, x=9, y=5, direction="W")
    resp = _cmd(client, "B")
    assert resp.status_code == 409
    assert resp.json()["blocked_by"] == "boundary"
    assert resp.json()["probe_state"]["position"] == {"x": 9, "y": 5}


# ---------------------------------------------------------------------------
# Feature: Obstacle Avoidance (US-04)
# ---------------------------------------------------------------------------


def test_obstacle_blocks_forward(client):
    """Scenario: Probe blocked by obstacle ahead when moving forward."""
    _init(client, x=0, y=0, direction="N", obstacles=[{"x": 0, "y": 2}])
    resp = _cmd(client, "F F F")
    assert resp.status_code == 409
    body = resp.json()
    assert body["blocked_by"] == "obstacle"
    assert body["blocked_at"] == {"x": 0, "y": 2}
    assert body["probe_state"]["position"] == {"x": 0, "y": 1}


def test_obstacle_blocks_backward(client):
    """Scenario: Probe blocked by obstacle when moving backward."""
    _init(client, x=0, y=5, direction="N", obstacles=[{"x": 0, "y": 3}])
    resp = _cmd(client, "B B B")
    assert resp.status_code == 409
    body = resp.json()
    assert body["blocked_by"] == "obstacle"
    assert body["blocked_at"] == {"x": 0, "y": 3}
    assert body["probe_state"]["position"] == {"x": 0, "y": 4}


def test_navigate_around_obstacle(client):
    """Scenario: Probe navigates around an obstacle."""
    _init(client, x=0, y=0, direction="N", obstacles=[{"x": 0, "y": 2}])
    resp = _cmd(client, "F R F L F")
    assert resp.status_code == 200
    state = resp.json()["probe_state"]
    assert state["position"] == {"x": 1, "y": 2}
    assert state["direction"] == "N"


def test_cannot_initialise_on_obstacle(client):
    """Scenario: Probe cannot be initialised on an obstacle."""
    resp = _init(client, x=3, y=3, obstacles=[{"x": 3, "y": 3}])
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_multiple_obstacles(client):
    """Scenario: Multiple obstacles on grid."""
    _init(client, x=0, y=0, direction="N",
          obstacles=[{"x": 2, "y": 2}, {"x": 4, "y": 4}])
    resp = _cmd(client, "F F R F F")
    assert resp.status_code == 409
    body = resp.json()
    assert body["blocked_by"] == "obstacle"
    assert body["probe_state"]["position"] == {"x": 1, "y": 2}


# ---------------------------------------------------------------------------
# Feature: Visit History (US-05)
# ---------------------------------------------------------------------------


def test_history_records_start(client):
    """Scenario: History records start position."""
    _init(client, x=0, y=0, direction="N")
    hist = client.get(HISTORY_URL).json()
    assert hist["visited"] == [{"x": 0, "y": 0}]


def test_history_records_moves(client):
    """Scenario: History records each position visited."""
    _init(client, x=0, y=0, direction="N")
    _cmd(client, "F F R F")
    hist = client.get(HISTORY_URL).json()
    assert hist["visited"] == [
        {"x": 0, "y": 0},
        {"x": 0, "y": 1},
        {"x": 0, "y": 2},
        {"x": 1, "y": 2},
    ]


def test_turns_not_in_history(client):
    """Scenario: Turns do not add new entries to history."""
    _init(client, x=0, y=0, direction="N")
    _cmd(client, "R R")
    hist = client.get(HISTORY_URL).json()
    assert hist["visited"] == [{"x": 0, "y": 0}]


def test_history_persists_across_requests(client):
    """Scenario: History persists across multiple command requests."""
    _init(client, x=0, y=0, direction="N")
    _cmd(client, "F F")
    _cmd(client, "R F")
    hist = client.get(HISTORY_URL).json()
    assert hist["visited"] == [
        {"x": 0, "y": 0},
        {"x": 0, "y": 1},
        {"x": 0, "y": 2},
        {"x": 1, "y": 2},
    ]


def test_history_resets_on_reinitialise(client):
    """Scenario: History resets on re-initialisation."""
    _init(client, x=3, y=3, direction="N")
    _cmd(client, "F F")
    _init(client, x=0, y=0, direction="N")
    hist = client.get(HISTORY_URL).json()
    assert hist["visited"] == [{"x": 0, "y": 0}]


def test_blocked_position_not_in_history(client):
    """Scenario: Blocked position is not added to history."""
    _init(client, x=0, y=1, direction="N", obstacles=[{"x": 0, "y": 2}])
    _cmd(client, "F")
    hist = client.get(HISTORY_URL).json()
    assert {"x": 0, "y": 2} not in hist["visited"]
    assert {"x": 0, "y": 1} in hist["visited"]


def test_revisiting_coordinate_recorded_each_time(client):
    """Scenario: Revisiting a coordinate is recorded each time."""
    _init(client, x=0, y=0, direction="N")
    _cmd(client, "F B")
    hist = client.get(HISTORY_URL).json()
    assert hist["visited"] == [
        {"x": 0, "y": 0},
        {"x": 0, "y": 1},
        {"x": 0, "y": 0},
    ]
    assert len(hist["visited"]) == 3


# ---------------------------------------------------------------------------
# Feature: API Session State (Global Edge Cases)
# ---------------------------------------------------------------------------


def test_commands_before_initialisation_rejected(client):
    """Scenario: Commands sent before initialisation are rejected."""
    resp = _cmd(client, "F F")
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_history_before_initialisation_rejected(client):
    """Scenario: History requested before initialisation is rejected."""
    resp = client.get(HISTORY_URL)
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_probe_state_query(client):
    """Scenario: Probe state can be queried without sending commands."""
    _init(client, x=3, y=4, direction="W")
    resp = client.get(STATE_URL)
    assert resp.status_code == 200
    body = resp.json()
    assert body["position"] == {"x": 3, "y": 4}
    assert body["direction"] == "W"


def test_health_endpoint(client):
    """Scenario: Health endpoint returns 200."""
    resp = client.get(HEALTH_URL)
    assert resp.status_code == 200
