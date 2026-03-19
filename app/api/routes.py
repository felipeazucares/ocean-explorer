"""FastAPI route handlers for Ocean Explorer API — Phase 5."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.domain.grid import Grid
from app.domain.probe import Probe
from app.models import (
    CommandRequest,
    CommandResponse,
    HistoryResponse,
    InitialiseRequest,
    Position,
    ProbeState,
    StateResponse,
)

router = APIRouter(prefix="/probe")

_NOT_INITIALISED = "Probe is not initialised"


def _validate_initialise(request: InitialiseRequest) -> None:
    """Validate initialise request; raise HTTPException(400) on failure."""
    if request.grid_width <= 0 or request.grid_height <= 0:
        raise HTTPException(status_code=400, detail="Grid dimensions must be positive")
    obs = [(o.x, o.y) for o in request.obstacles]
    for ox, oy in obs:
        if not (0 <= ox < request.grid_width and 0 <= oy < request.grid_height):
            raise HTTPException(
                status_code=400, detail=f"Obstacle ({ox},{oy}) is outside grid bounds"
            )
    if not (0 <= request.x < request.grid_width and 0 <= request.y < request.grid_height):
        raise HTTPException(
            status_code=400,
            detail=f"Position ({request.x},{request.y}) is outside grid bounds",
        )
    if (request.x, request.y) in set(obs):
        raise HTTPException(
            status_code=400,
            detail=f"Starting position ({request.x},{request.y}) conflicts with obstacle",
        )


@router.post("/initialise", response_model=StateResponse)
def initialise_probe(request: InitialiseRequest) -> StateResponse:
    """Initialise probe at given position and direction on the grid."""
    _validate_initialise(request)
    import app.main as main  # avoid circular import at module level

    obstacles = [(o.x, o.y) for o in request.obstacles]
    grid = Grid(request.grid_width, request.grid_height, obstacles)
    main.probe = Probe(request.x, request.y, request.direction, grid)
    return StateResponse(
        position=Position(x=main.probe.x, y=main.probe.y),
        direction=main.probe.direction,
    )


@router.post("/commands")
def run_commands(request: CommandRequest) -> JSONResponse:
    """Execute command sequence on probe; return 409 if blocked."""
    import app.main as main  # avoid circular import at module level

    if main.probe is None:
        raise HTTPException(status_code=400, detail=_NOT_INITIALISED)
    result = main.probe.execute(request.commands)
    blocked_at = (
        Position(x=result.blocked_at[0], y=result.blocked_at[1])
        if result.blocked_at
        else None
    )
    response_body = CommandResponse(
        probe_state=ProbeState(
            position=Position(x=main.probe.x, y=main.probe.y),
            direction=main.probe.direction,
        ),
        blocked_by=result.blocked_by,
        blocked_at=blocked_at,
        visited=[Position(x=x, y=y) for x, y in main.probe.history],
    )
    status_code = 409 if result.blocked_by else 200
    return JSONResponse(content=response_body.model_dump(), status_code=status_code)


@router.get("/history", response_model=HistoryResponse)
def get_history() -> HistoryResponse:
    """Return full visit history and current probe state."""
    import app.main as main  # avoid circular import at module level

    if main.probe is None:
        raise HTTPException(status_code=400, detail=_NOT_INITIALISED)
    return HistoryResponse(
        position=Position(x=main.probe.x, y=main.probe.y),
        direction=main.probe.direction,
        visited=[Position(x=x, y=y) for x, y in main.probe.history],
    )


@router.get("/state", response_model=StateResponse)
def get_state() -> StateResponse:
    """Return current probe position and direction."""
    import app.main as main  # avoid circular import at module level

    if main.probe is None:
        raise HTTPException(status_code=400, detail=_NOT_INITIALISED)
    return StateResponse(
        position=Position(x=main.probe.x, y=main.probe.y),
        direction=main.probe.direction,
    )
