"""Unit tests for the Probe domain class (Phase 4)."""
import pytest
from app.domain.grid import Grid
from app.domain.probe import Probe
from app.models import CommandEnum, DirectionEnum


class TestProbeInitialisation:
    """Probe initialises with correct state."""

    def test_initialises_at_correct_position(self):
        grid = Grid(10, 10)
        probe = Probe(3, 5, DirectionEnum.EAST, grid)
        assert probe.x == 3
        assert probe.y == 5

    def test_initialises_with_correct_direction(self):
        grid = Grid(10, 10)
        probe = Probe(0, 0, DirectionEnum.NORTH, grid)
        assert probe.direction == DirectionEnum.NORTH

    def test_records_start_position_in_history(self):
        grid = Grid(10, 10)
        probe = Probe(2, 4, DirectionEnum.SOUTH, grid)
        assert probe.history == [(2, 4)]


class TestMoveForward:
    """Forward movement updates position in the facing direction."""

    def test_move_forward_facing_north(self):
        grid = Grid(10, 10)
        probe = Probe(0, 0, DirectionEnum.NORTH, grid)
        probe.execute([CommandEnum.FORWARD])
        assert probe.x == 0
        assert probe.y == 1

    def test_move_forward_facing_south(self):
        grid = Grid(10, 10)
        probe = Probe(5, 5, DirectionEnum.SOUTH, grid)
        probe.execute([CommandEnum.FORWARD])
        assert probe.x == 5
        assert probe.y == 4

    def test_move_forward_facing_east(self):
        grid = Grid(10, 10)
        probe = Probe(5, 5, DirectionEnum.EAST, grid)
        probe.execute([CommandEnum.FORWARD])
        assert probe.x == 6
        assert probe.y == 5

    def test_move_forward_facing_west(self):
        grid = Grid(10, 10)
        probe = Probe(5, 5, DirectionEnum.WEST, grid)
        probe.execute([CommandEnum.FORWARD])
        assert probe.x == 4
        assert probe.y == 5


class TestMoveBackward:
    """Backward movement updates position opposite to the facing direction."""

    def test_move_backward_facing_north(self):
        grid = Grid(10, 10)
        probe = Probe(5, 5, DirectionEnum.NORTH, grid)
        probe.execute([CommandEnum.BACKWARD])
        assert probe.x == 5
        assert probe.y == 4

    def test_move_backward_facing_south(self):
        grid = Grid(10, 10)
        probe = Probe(5, 5, DirectionEnum.SOUTH, grid)
        probe.execute([CommandEnum.BACKWARD])
        assert probe.x == 5
        assert probe.y == 6


class TestTurns:
    """Turns update direction only — position and history are unchanged."""

    def test_turn_left_updates_direction_only(self):
        grid = Grid(10, 10)
        probe = Probe(3, 3, DirectionEnum.NORTH, grid)
        probe.execute([CommandEnum.LEFT])
        assert probe.direction == DirectionEnum.WEST
        assert probe.x == 3
        assert probe.y == 3

    def test_turn_right_updates_direction_only(self):
        grid = Grid(10, 10)
        probe = Probe(3, 3, DirectionEnum.NORTH, grid)
        probe.execute([CommandEnum.RIGHT])
        assert probe.direction == DirectionEnum.EAST
        assert probe.x == 3
        assert probe.y == 3

    def test_turns_do_not_add_to_history(self):
        grid = Grid(10, 10)
        probe = Probe(0, 0, DirectionEnum.NORTH, grid)
        probe.execute([CommandEnum.LEFT, CommandEnum.RIGHT])
        assert probe.history == [(0, 0)]


class TestVisitHistory:
    """Visit history records positions correctly."""

    def test_moves_add_to_history(self):
        grid = Grid(10, 10)
        probe = Probe(0, 0, DirectionEnum.NORTH, grid)
        probe.execute([CommandEnum.FORWARD])
        assert probe.history == [(0, 0), (0, 1)]

    def test_history_cumulative_across_execute_calls(self):
        grid = Grid(10, 10)
        probe = Probe(0, 0, DirectionEnum.NORTH, grid)
        probe.execute([CommandEnum.FORWARD, CommandEnum.FORWARD])
        probe.execute([CommandEnum.RIGHT, CommandEnum.FORWARD])
        assert probe.history == [(0, 0), (0, 1), (0, 2), (1, 2)]

    def test_blocked_position_not_added_to_history(self):
        grid = Grid(10, 10, [(0, 2)])
        probe = Probe(0, 1, DirectionEnum.NORTH, grid)
        probe.execute([CommandEnum.FORWARD])
        assert (0, 2) not in probe.history


class TestBoundaryBlocking:
    """Probe halts at boundary and reports the reason."""

    def test_probe_stops_at_boundary(self):
        grid = Grid(10, 10)
        probe = Probe(0, 9, DirectionEnum.NORTH, grid)
        probe.execute([CommandEnum.FORWARD])
        assert probe.x == 0
        assert probe.y == 9

    def test_boundary_block_reports_reason(self):
        grid = Grid(10, 10)
        probe = Probe(0, 9, DirectionEnum.NORTH, grid)
        result = probe.execute([CommandEnum.FORWARD])
        assert result.blocked_by == "boundary"

    def test_commands_after_boundary_block_not_executed(self):
        grid = Grid(10, 10)
        probe = Probe(0, 9, DirectionEnum.NORTH, grid)
        probe.execute([CommandEnum.FORWARD, CommandEnum.FORWARD, CommandEnum.FORWARD])
        assert probe.x == 0
        assert probe.y == 9


class TestObstacleBlocking:
    """Probe halts at obstacle and reports the reason and position."""

    def test_probe_stops_before_obstacle(self):
        grid = Grid(10, 10, [(0, 2)])
        probe = Probe(0, 0, DirectionEnum.NORTH, grid)
        probe.execute([CommandEnum.FORWARD, CommandEnum.FORWARD, CommandEnum.FORWARD])
        assert probe.x == 0
        assert probe.y == 1

    def test_obstacle_block_reports_reason(self):
        grid = Grid(10, 10, [(0, 2)])
        probe = Probe(0, 0, DirectionEnum.NORTH, grid)
        result = probe.execute([CommandEnum.FORWARD, CommandEnum.FORWARD, CommandEnum.FORWARD])
        assert result.blocked_by == "obstacle"

    def test_obstacle_block_reports_obstacle_position(self):
        grid = Grid(10, 10, [(0, 2)])
        probe = Probe(0, 0, DirectionEnum.NORTH, grid)
        result = probe.execute([CommandEnum.FORWARD, CommandEnum.FORWARD, CommandEnum.FORWARD])
        assert result.blocked_at == (0, 2)

    def test_commands_after_obstacle_block_not_executed(self):
        grid = Grid(10, 10, [(0, 2)])
        probe = Probe(0, 0, DirectionEnum.NORTH, grid)
        probe.execute([CommandEnum.FORWARD, CommandEnum.FORWARD, CommandEnum.FORWARD])
        assert probe.x == 0
        assert probe.y == 1


class TestExecuteSequence:
    """Multi-command sequences execute correctly end-to-end."""

    def test_sequence_F_F_R_F_from_origin_north(self):
        grid = Grid(10, 10)
        probe = Probe(0, 0, DirectionEnum.NORTH, grid)
        probe.execute([
            CommandEnum.FORWARD,
            CommandEnum.FORWARD,
            CommandEnum.RIGHT,
            CommandEnum.FORWARD,
        ])
        assert probe.x == 1
        assert probe.y == 2
        assert probe.direction == DirectionEnum.EAST
