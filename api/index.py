"""Vercel entry point: exposes the FastAPI app as a serverless function.
Local development still runs `uvicorn app.main:app` from this folder."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app  # noqa: E402,F401
