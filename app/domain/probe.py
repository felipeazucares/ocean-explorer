"""Probe domain class — encapsulates probe state and command execution."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from app.domain.direction import Direction
from app.domain.grid import Grid
from app.models import BlockReasonEnum, CommandEnum, DirectionEnum


@dataclass
class ExecuteResult:
    """Result returned by Probe.execute()."""

    blocked_by: Optional[BlockReasonEnum] = None
    blocked_at: Optional[tuple[int, int]] = None


class Probe:
    """Encapsulates probe state: position, direction, and visit history."""

    def __init__(self, x: int, y: int, direction: DirectionEnum, grid: Grid) -> None:
        """Initialise probe at (x, y) facing direction on the given grid."""
        self._x = x
        self._y = y
        self._direction = Direction(direction)
        self._grid = grid
        self._history: list[tuple[int, int]] = [(x, y)]

    @property
    def x(self) -> int:
        """Current x coordinate."""
        return self._x

    @property
    def y(self) -> int:
        """Current y coordinate."""
        return self._y

    @property
    def direction(self) -> DirectionEnum:
        """Current facing direction."""
        return self._direction.value

    @property
    def history(self) -> list[tuple[int, int]]:
        """Ordered list of all positions occupied (including start)."""
        return list(self._history)

    def execute(self, commands: list[CommandEnum]) -> ExecuteResult:
        """Execute a sequence of commands; halt on first block."""
        for command in commands:
            result = self._execute_one(command)
            if result.blocked_by:
                return result
        return ExecuteResult()

    def _execute_one(self, command: CommandEnum) -> ExecuteResult:
        """Execute a single command; return ExecuteResult (blocked or clear)."""
        if command == CommandEnum.LEFT:
            self._direction = self._direction.turn_left()
            return ExecuteResult()
        if command == CommandEnum.RIGHT:
            self._direction = self._direction.turn_right()
            return ExecuteResult()
        forward = command == CommandEnum.FORWARD
        nx, ny = self._direction.next_position(self._x, self._y, forward=forward)
        if not self._grid.is_valid(nx, ny):
            return self._build_block_result(nx, ny)
        self._x, self._y = nx, ny
        self._history.append((self._x, self._y))
        return ExecuteResult()

    def _build_block_result(self, nx: int, ny: int) -> ExecuteResult:
        """Return the correct block reason for position (nx, ny)."""
        if self._grid.is_boundary_block(nx, ny):
            return ExecuteResult(blocked_by=BlockReasonEnum.BOUNDARY)
        return ExecuteResult(blocked_by=BlockReasonEnum.OBSTACLE, blocked_at=(nx, ny))
