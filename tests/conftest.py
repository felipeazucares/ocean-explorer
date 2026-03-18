"""Shared test fixtures for Ocean Explorer."""

import pytest

from app.main import app

try:
    from httpx import ASGITransport
except ImportError:
    ASGITransport = None

from httpx import AsyncClient


@pytest.fixture()
def client():
    """Create a TestClient for integration and acceptance tests."""
    from fastapi.testclient import TestClient

    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def _reset_probe_state():
    """Reset probe state before each test to ensure isolation.

    The probe lives as a single in-memory instance on the server.
    Without this fixture, state leaks between tests.
    """
    from app import main

    main.probe = None
    yield
    main.probe = None
