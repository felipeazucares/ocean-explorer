"""Integration tests for Ocean Explorer API endpoints — Phase 5."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

INIT_URL = "/probe/initialise"
CMD_URL = "/probe/commands"
HISTORY_URL = "/probe/history"
STATE_URL = "/probe/state"

VALID_INIT = {"x": 0, "y": 0, "direction": "N", "grid_width": 10, "grid_height": 10}


def init(client, **overrides):
    """POST /probe/initialise with VALID_INIT merged with overrides."""
    return client.post(INIT_URL, json={**VALID_INIT, **overrides})


def commands(client, cmds: list[str]):
    """POST /probe/commands with a list of command strings."""
    return client.post(CMD_URL, json={"commands": cmds})


# ---------------------------------------------------------------------------
# POST /probe/initialise
# ---------------------------------------------------------------------------


def test_initialise_returns_200_valid_request(client):
    """Valid initialisation returns 200 with position and direction."""
    resp = init(client)
    assert resp.status_code == 200
    body = resp.json()
    assert body["position"] == {"x": 0, "y": 0}
    assert body["direction"] == "N"


def test_initialise_returns_400_out_of_bounds_position(client):
    """Position outside grid is rejected with 400."""
    resp = init(client, x=10, y=10)
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_initialise_returns_400_negative_x(client):
    """Negative x coordinate is rejected with 400."""
    resp = init(client, x=-1, y=0)
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_initialise_returns_400_negative_y(client):
    """Negative y coordinate is rejected with 400."""
    resp = init(client, x=0, y=-1)
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_initialise_returns_400_invalid_direction(client):
    """Invalid direction value is rejected with 400."""
    resp = client.post(INIT_URL, json={**VALID_INIT, "direction": "X"})
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_initialise_returns_400_position_on_obstacle(client):
    """Starting position on an obstacle is rejected with 400."""
    resp = init(client, x=3, y=3, obstacles=[{"x": 3, "y": 3}])
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_initialise_returns_400_zero_width_grid(client):
    """Zero-width grid is rejected with 400."""
    resp = init(client, grid_width=0)
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_initialise_returns_400_zero_height_grid(client):
    """Zero-height grid is rejected with 400."""
    resp = init(client, grid_height=0)
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_initialise_returns_400_obstacle_outside_grid(client):
    """Obstacle outside grid bounds is rejected with 400."""
    resp = init(client, obstacles=[{"x": 15, "y": 15}])
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_initialise_response_conforms_to_state_response(client):
    """Initialisation response matches StateResponse schema."""
    resp = init(client, x=5, y=7, direction="E")
    assert resp.status_code == 200
    body = resp.json()
    assert body["position"] == {"x": 5, "y": 7}
    assert body["direction"] == "E"


# ---------------------------------------------------------------------------
# POST /probe/commands
# ---------------------------------------------------------------------------


def test_commands_returns_200_valid_sequence(client):
    """Valid command sequence returns 200 with updated probe state."""
    init(client)
    resp = commands(client, ["F", "F"])
    assert resp.status_code == 200
    body = resp.json()
    assert body["probe_state"]["position"] == {"x": 0, "y": 2}
    assert body["probe_state"]["direction"] == "N"
    assert "visited" in body


def test_commands_returns_200_empty_sequence(client):
    """Empty command sequence returns 200 with unchanged probe state."""
    init(client, x=3, y=3, direction="E")
    resp = commands(client, [])
    assert resp.status_code == 200
    body = resp.json()
    assert body["probe_state"]["position"] == {"x": 3, "y": 3}
    assert body["probe_state"]["direction"] == "E"


def test_commands_returns_400_invalid_command(client):
    """Invalid command character is rejected with 400."""
    init(client)
    resp = client.post(CMD_URL, json={"commands": ["F", "X", "F"]})
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_commands_returns_400_probe_not_initialised(client):
    """Commands sent before initialisation are rejected with 400."""
    resp = commands(client, ["F"])
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_commands_returns_409_blocked_by_boundary(client):
    """Move into boundary returns 409 with blocked_by boundary."""
    init(client, x=0, y=9, direction="N")
    resp = commands(client, ["F"])
    assert resp.status_code == 409
    body = resp.json()
    assert body["blocked_by"] == "boundary"
    assert body["probe_state"]["position"] == {"x": 0, "y": 9}


def test_commands_returns_409_blocked_by_obstacle(client):
    """Move into obstacle returns 409 with blocked_by obstacle and blocked_at."""
    init(client, x=0, y=0, direction="N", obstacles=[{"x": 0, "y": 2}])
    resp = commands(client, ["F", "F", "F"])
    assert resp.status_code == 409
    body = resp.json()
    assert body["blocked_by"] == "obstacle"
    assert body["blocked_at"] == {"x": 0, "y": 2}
    assert body["probe_state"]["position"] == {"x": 0, "y": 1}


def test_commands_response_conforms_to_command_response(client):
    """Command response matches CommandResponse schema."""
    init(client)
    resp = commands(client, ["F", "R", "F"])
    assert resp.status_code == 200
    body = resp.json()
    assert "probe_state" in body
    assert "visited" in body
    assert isinstance(body["visited"], list)


# ---------------------------------------------------------------------------
# GET /probe/history
# ---------------------------------------------------------------------------


def test_history_returns_200_with_visit_list(client):
    """History endpoint returns 200 with ordered visit list."""
    init(client)
    commands(client, ["F", "F"])
    resp = client.get(HISTORY_URL)
    assert resp.status_code == 200
    body = resp.json()
    assert body["visited"] == [
        {"x": 0, "y": 0},
        {"x": 0, "y": 1},
        {"x": 0, "y": 2},
    ]


def test_history_returns_400_probe_not_initialised(client):
    """History request before initialisation is rejected with 400."""
    resp = client.get(HISTORY_URL)
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_history_response_conforms_to_history_response(client):
    """History response matches HistoryResponse schema."""
    init(client, x=2, y=3, direction="S")
    resp = client.get(HISTORY_URL)
    assert resp.status_code == 200
    body = resp.json()
    assert body["position"] == {"x": 2, "y": 3}
    assert body["direction"] == "S"
    assert isinstance(body["visited"], list)


# ---------------------------------------------------------------------------
# GET /probe/state
# ---------------------------------------------------------------------------


def test_state_returns_200_with_position_and_direction(client):
    """State endpoint returns 200 with current probe position and direction."""
    init(client, x=3, y=4, direction="W")
    resp = client.get(STATE_URL)
    assert resp.status_code == 200
    body = resp.json()
    assert body["position"] == {"x": 3, "y": 4}
    assert body["direction"] == "W"


def test_state_returns_400_probe_not_initialised(client):
    """State request before initialisation is rejected with 400."""
    resp = client.get(STATE_URL)
    assert resp.status_code == 400
    assert "detail" in resp.json()


def test_state_response_conforms_to_state_response(client):
    """State response matches StateResponse schema."""
    init(client)
    commands(client, ["F", "R"])
    resp = client.get(STATE_URL)
    assert resp.status_code == 200
    body = resp.json()
    assert "position" in body
    assert "direction" in body
