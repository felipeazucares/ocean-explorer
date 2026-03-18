"""Direction domain class — encapsulates compass direction and movement deltas."""
from app.models import DirectionEnum

_TURN_RIGHT = {
    DirectionEnum.NORTH: DirectionEnum.EAST,
    DirectionEnum.EAST: DirectionEnum.SOUTH,
    DirectionEnum.SOUTH: DirectionEnum.WEST,
    DirectionEnum.WEST: DirectionEnum.NORTH,
}

_TURN_LEFT = {v: k for k, v in _TURN_RIGHT.items()}

_FORWARD_DELTA = {
    DirectionEnum.NORTH: (0, 1),
    DirectionEnum.SOUTH: (0, -1),
    DirectionEnum.EAST: (1, 0),
    DirectionEnum.WEST: (-1, 0),
}


class Direction:
    """Encapsulates a compass direction and related movement calculations."""

    def __init__(self, value: DirectionEnum) -> None:
        """Initialise with a DirectionEnum value."""
        self.value = value

    def turn_right(self) -> "Direction":
        """Return a new Direction rotated 90 degrees clockwise."""
        return Direction(_TURN_RIGHT[self.value])

    def turn_left(self) -> "Direction":
        """Return a new Direction rotated 90 degrees anticlockwise."""
        return Direction(_TURN_LEFT[self.value])

    def next_position(self, x: int, y: int, *, forward: bool) -> tuple[int, int]:
        """Return (x, y) after one step; forward=False inverts the delta."""
        dx, dy = _FORWARD_DELTA[self.value]
        if not forward:
            dx, dy = -dx, -dy
        return x + dx, y + dy
