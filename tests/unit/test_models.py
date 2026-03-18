"""Unit tests for Pydantic models and enums (Phase 1)."""
import pytest
from pydantic import ValidationError


# ---------------------------------------------------------------------------
# DirectionEnum
# ---------------------------------------------------------------------------

class TestDirectionEnum:
    """Tests for DirectionEnum values and membership."""

    def test_north_value(self):
        from app.models import DirectionEnum
        assert DirectionEnum.NORTH == "N"

    def test_south_value(self):
        from app.models import DirectionEnum
        assert DirectionEnum.SOUTH == "S"

    def test_east_value(self):
        from app.models import DirectionEnum
        assert DirectionEnum.EAST == "E"

    def test_west_value(self):
        from app.models import DirectionEnum
        assert DirectionEnum.WEST == "W"

    def test_invalid_direction_not_in_enum(self):
        from app.models import DirectionEnum
        with pytest.raises(ValueError):
            DirectionEnum("X")

    def test_all_four_directions_present(self):
        from app.models import DirectionEnum
        assert set(DirectionEnum) == {
            DirectionEnum.NORTH, DirectionEnum.SOUTH,
            DirectionEnum.EAST, DirectionEnum.WEST,
        }


# ---------------------------------------------------------------------------
# CommandEnum
# ---------------------------------------------------------------------------

class TestCommandEnum:
    """Tests for CommandEnum values and membership."""

    def test_forward_value(self):
        from app.models import CommandEnum
        assert CommandEnum.FORWARD == "F"

    def test_backward_value(self):
        from app.models import CommandEnum
        assert CommandEnum.BACKWARD == "B"

    def test_left_value(self):
        from app.models import CommandEnum
        assert CommandEnum.LEFT == "L"

    def test_right_value(self):
        from app.models import CommandEnum
        assert CommandEnum.RIGHT == "R"

    def test_invalid_command_not_in_enum(self):
        from app.models import CommandEnum
        with pytest.raises(ValueError):
            CommandEnum("X")


# ---------------------------------------------------------------------------
# InitialiseRequest
# ---------------------------------------------------------------------------

class TestInitialiseRequest:
    """Tests for InitialiseRequest validation."""

    def test_valid_minimal_request(self):
        from app.models import InitialiseRequest, DirectionEnum
        req = InitialiseRequest(x=0, y=0, direction=DirectionEnum.NORTH)
        assert req.x == 0
        assert req.y == 0
        assert req.direction == DirectionEnum.NORTH

    def test_default_grid_width(self):
        from app.models import InitialiseRequest, DirectionEnum
        req = InitialiseRequest(x=0, y=0, direction=DirectionEnum.NORTH)
        assert req.grid_width == 10

    def test_default_grid_height(self):
        from app.models import InitialiseRequest, DirectionEnum
        req = InitialiseRequest(x=0, y=0, direction=DirectionEnum.NORTH)
        assert req.grid_height == 10

    def test_default_obstacles_empty(self):
        from app.models import InitialiseRequest, DirectionEnum
        req = InitialiseRequest(x=0, y=0, direction=DirectionEnum.NORTH)
        assert req.obstacles == []

    def test_custom_grid_dimensions(self):
        from app.models import InitialiseRequest, DirectionEnum
        req = InitialiseRequest(
            x=0, y=0, direction=DirectionEnum.NORTH,
            grid_width=20, grid_height=15,
        )
        assert req.grid_width == 20
        assert req.grid_height == 15

    def test_obstacles_accepted(self):
        from app.models import InitialiseRequest, DirectionEnum, Position
        req = InitialiseRequest(
            x=0, y=0, direction=DirectionEnum.NORTH,
            obstacles=[Position(x=3, y=4), Position(x=5, y=5)],
        )
        assert len(req.obstacles) == 2

    def test_direction_string_coercion(self):
        from app.models import InitialiseRequest, DirectionEnum
        req = InitialiseRequest(x=0, y=0, direction="N")
        assert req.direction == DirectionEnum.NORTH

    def test_invalid_direction_raises(self):
        from app.models import InitialiseRequest
        with pytest.raises(ValidationError):
            InitialiseRequest(x=0, y=0, direction="X")


# ---------------------------------------------------------------------------
# CommandRequest
# ---------------------------------------------------------------------------

class TestCommandRequest:
    """Tests for CommandRequest validation."""

    def test_valid_commands(self):
        from app.models import CommandRequest, CommandEnum
        req = CommandRequest(commands=[CommandEnum.FORWARD, CommandEnum.RIGHT])
        assert req.commands == [CommandEnum.FORWARD, CommandEnum.RIGHT]

    def test_empty_commands_allowed(self):
        from app.models import CommandRequest
        req = CommandRequest(commands=[])
        assert req.commands == []

    def test_command_string_coercion(self):
        from app.models import CommandRequest, CommandEnum
        req = CommandRequest(commands=["F", "B", "L", "R"])
        assert req.commands == [
            CommandEnum.FORWARD, CommandEnum.BACKWARD,
            CommandEnum.LEFT, CommandEnum.RIGHT,
        ]

    def test_invalid_command_raises(self):
        from app.models import CommandRequest
        with pytest.raises(ValidationError):
            CommandRequest(commands=["F", "X", "F"])


# ---------------------------------------------------------------------------
# Position
# ---------------------------------------------------------------------------

class TestPosition:
    """Tests for Position model."""

    def test_valid_position(self):
        from app.models import Position
        pos = Position(x=3, y=7)
        assert pos.x == 3
        assert pos.y == 7

    def test_zero_position(self):
        from app.models import Position
        pos = Position(x=0, y=0)
        assert pos.x == 0
        assert pos.y == 0


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------

class TestProbeState:
    """Tests for ProbeState model."""

    def test_valid_probe_state(self):
        from app.models import ProbeState, Position, DirectionEnum
        state = ProbeState(
            position=Position(x=1, y=2),
            direction=DirectionEnum.EAST,
        )
        assert state.position.x == 1
        assert state.direction == DirectionEnum.EAST


class TestCommandResponse:
    """Tests for CommandResponse model."""

    def test_unblocked_response(self):
        from app.models import CommandResponse, ProbeState, Position, DirectionEnum
        resp = CommandResponse(
            probe_state=ProbeState(
                position=Position(x=1, y=1),
                direction=DirectionEnum.NORTH,
            ),
            visited=[Position(x=0, y=0), Position(x=1, y=1)],
        )
        assert resp.blocked_by is None
        assert resp.blocked_at is None
        assert len(resp.visited) == 2

    def test_blocked_by_boundary(self):
        from app.models import CommandResponse, ProbeState, Position, DirectionEnum
        resp = CommandResponse(
            probe_state=ProbeState(
                position=Position(x=0, y=9),
                direction=DirectionEnum.NORTH,
            ),
            blocked_by="boundary",
            visited=[Position(x=0, y=9)],
        )
        assert resp.blocked_by == "boundary"
        assert resp.blocked_at is None

    def test_blocked_by_obstacle(self):
        from app.models import CommandResponse, ProbeState, Position, DirectionEnum
        resp = CommandResponse(
            probe_state=ProbeState(
                position=Position(x=0, y=1),
                direction=DirectionEnum.NORTH,
            ),
            blocked_by="obstacle",
            blocked_at=Position(x=0, y=2),
            visited=[Position(x=0, y=0), Position(x=0, y=1)],
        )
        assert resp.blocked_by == "obstacle"
        assert resp.blocked_at.x == 0
        assert resp.blocked_at.y == 2


class TestHistoryResponse:
    """Tests for HistoryResponse model."""

    def test_history_response(self):
        from app.models import HistoryResponse, Position, DirectionEnum
        resp = HistoryResponse(
            position=Position(x=2, y=3),
            direction=DirectionEnum.WEST,
            visited=[Position(x=0, y=0), Position(x=2, y=3)],
        )
        assert len(resp.visited) == 2
        assert resp.direction == DirectionEnum.WEST


class TestStateResponse:
    """Tests for StateResponse model."""

    def test_state_response(self):
        from app.models import StateResponse, Position, DirectionEnum
        resp = StateResponse(
            position=Position(x=5, y=5),
            direction=DirectionEnum.SOUTH,
        )
        assert resp.position.x == 5
        assert resp.direction == DirectionEnum.SOUTH


class TestErrorResponse:
    """Tests for ErrorResponse model."""

    def test_error_response(self):
        from app.models import ErrorResponse
        resp = ErrorResponse(detail="something went wrong")
        assert resp.detail == "something went wrong"
