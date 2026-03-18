"""Unit tests for Direction domain class — Phase 2."""
from app.domain.direction import Direction
from app.models import DirectionEnum


class TestTurnRight:
    """turn_right returns the correct direction for each compass point."""

    def test_turn_right_from_north(self):
        d = Direction(DirectionEnum.NORTH)
        assert d.turn_right().value == DirectionEnum.EAST

    def test_turn_right_from_east(self):
        d = Direction(DirectionEnum.EAST)
        assert d.turn_right().value == DirectionEnum.SOUTH

    def test_turn_right_from_south(self):
        d = Direction(DirectionEnum.SOUTH)
        assert d.turn_right().value == DirectionEnum.WEST

    def test_turn_right_from_west(self):
        d = Direction(DirectionEnum.WEST)
        assert d.turn_right().value == DirectionEnum.NORTH


class TestTurnLeft:
    """turn_left returns the correct direction for each compass point."""

    def test_turn_left_from_north(self):
        d = Direction(DirectionEnum.NORTH)
        assert d.turn_left().value == DirectionEnum.WEST

    def test_turn_left_from_west(self):
        d = Direction(DirectionEnum.WEST)
        assert d.turn_left().value == DirectionEnum.SOUTH

    def test_turn_left_from_south(self):
        d = Direction(DirectionEnum.SOUTH)
        assert d.turn_left().value == DirectionEnum.EAST

    def test_turn_left_from_east(self):
        d = Direction(DirectionEnum.EAST)
        assert d.turn_left().value == DirectionEnum.NORTH


class TestFullRotation:
    """Four consecutive turns return to the original direction."""

    def test_full_clockwise_rotation(self):
        d = Direction(DirectionEnum.NORTH)
        for _ in range(4):
            d = d.turn_right()
        assert d.value == DirectionEnum.NORTH

    def test_full_anticlockwise_rotation(self):
        d = Direction(DirectionEnum.NORTH)
        for _ in range(4):
            d = d.turn_left()
        assert d.value == DirectionEnum.NORTH


class TestNextPositionForward:
    """next_position computes the correct forward delta."""

    def test_forward_north(self):
        d = Direction(DirectionEnum.NORTH)
        assert d.next_position(0, 0, forward=True) == (0, 1)

    def test_forward_south(self):
        d = Direction(DirectionEnum.SOUTH)
        assert d.next_position(0, 0, forward=True) == (0, -1)

    def test_forward_east(self):
        d = Direction(DirectionEnum.EAST)
        assert d.next_position(0, 0, forward=True) == (1, 0)

    def test_forward_west(self):
        d = Direction(DirectionEnum.WEST)
        assert d.next_position(0, 0, forward=True) == (-1, 0)


class TestNextPositionBackward:
    """next_position backward is the inverse of forward."""

    def test_backward_north(self):
        d = Direction(DirectionEnum.NORTH)
        assert d.next_position(0, 0, forward=False) == (0, -1)

    def test_backward_south(self):
        d = Direction(DirectionEnum.SOUTH)
        assert d.next_position(0, 0, forward=False) == (0, 1)

    def test_backward_east(self):
        d = Direction(DirectionEnum.EAST)
        assert d.next_position(0, 0, forward=False) == (-1, 0)

    def test_backward_west(self):
        d = Direction(DirectionEnum.WEST)
        assert d.next_position(0, 0, forward=False) == (1, 0)
