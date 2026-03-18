"""Grid domain class — encapsulates grid dimensions and obstacle positions."""
from __future__ import annotations


class Grid:
    """Represents the bounded ocean floor grid."""

    def __init__(
        self,
        width: int,
        height: int,
        obstacles: list[tuple[int, int]] | None = None,
    ) -> None:
        """Initialise grid with given dimensions and optional obstacle set."""
        self.width = width
        self.height = height
        self._obstacles: frozenset[tuple[int, int]] = frozenset(obstacles or [])

    def _in_bounds(self, x: int, y: int) -> bool:
        """Return True if (x, y) is within grid boundaries."""
        return 0 <= x < self.width and 0 <= y < self.height

    def has_obstacle(self, x: int, y: int) -> bool:
        """Return True if (x, y) contains an obstacle."""
        return (x, y) in self._obstacles

    def is_valid(self, x: int, y: int) -> bool:
        """Return True if (x, y) is in bounds and free of obstacles."""
        return self._in_bounds(x, y) and not self.has_obstacle(x, y)

    def is_boundary_block(self, x: int, y: int) -> bool:
        """Return True if (x, y) is blocked by a grid boundary."""
        return not self._in_bounds(x, y)

    def is_obstacle_block(self, x: int, y: int) -> bool:
        """Return True if (x, y) is blocked by an obstacle (in bounds)."""
        return self._in_bounds(x, y) and self.has_obstacle(x, y)
