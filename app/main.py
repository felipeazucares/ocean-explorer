"""Ocean Explorer API application."""

from fastapi import FastAPI

app = FastAPI(title="Ocean Explorer", version="0.1.0")

# In-memory probe state (reset between tests via conftest.py)
probe = None
