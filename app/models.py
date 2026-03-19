"""Pydantic models and enums for the Ocean Explorer API (Phase 1)."""
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class DirectionEnum(str, Enum):
    """Compass directions the probe can face."""

    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"


class CommandEnum(str, Enum):
    """Movement and turn commands accepted by the probe."""

    FORWARD = "F"
    BACKWARD = "B"
    LEFT = "L"
    RIGHT = "R"


class BlockReasonEnum(str, Enum):
    """Reasons a probe move can be blocked."""

    BOUNDARY = "boundary"
    OBSTACLE = "obstacle"


class Position(BaseModel):
    """An x/y coordinate on the grid."""

    x: int
    y: int


class InitialiseRequest(BaseModel):
    """Request body for POST /probe/initialise."""

    x: int
    y: int
    direction: DirectionEnum
    grid_width: int = 10
    grid_height: int = 10
    obstacles: list[Position] = []


class CommandRequest(BaseModel):
    """Request body for POST /probe/commands."""

    commands: list[CommandEnum]


class ProbeState(BaseModel):
    """Current position and heading of the probe."""

    position: Position
    direction: DirectionEnum


class CommandResponse(BaseModel):
    """Response body for POST /probe/commands."""

    probe_state: ProbeState
    blocked_by: Optional[BlockReasonEnum] = None
    blocked_at: Optional[Position] = None
    visited: list[Position]


class HistoryResponse(BaseModel):
    """Response body for GET /probe/history."""

    position: Position
    direction: DirectionEnum
    visited: list[Position]


class StateResponse(BaseModel):
    """Response body for GET /probe/state."""

    position: Position
    direction: DirectionEnum


class ErrorResponse(BaseModel):
    """Response body for error conditions."""

    detail: str
