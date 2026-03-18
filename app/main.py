"""Ocean Explorer API application — Phase 5."""

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routes import router

logger = logging.getLogger(__name__)

app = FastAPI(title="Ocean Explorer", version="0.1.0")

# In-memory probe state (reset between tests via conftest.py autouse fixture)
probe = None


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Convert Pydantic validation errors to 400 instead of FastAPI default 422."""
    logger.error("Validation error on %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(status_code=400, content={"detail": str(exc.errors())})


@app.middleware("http")
async def log_requests(request: Request, call_next) -> JSONResponse:
    """Log all incoming requests and outgoing responses at INFO level."""
    logger.info("Request  %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("Response %s %s → %s", request.method, request.url.path, response.status_code)
    return response


@app.get("/health")
def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}


app.include_router(router)
