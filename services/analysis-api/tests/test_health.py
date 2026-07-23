"""Phase 1 application smoke tests."""

import asyncio

import httpx
from app.main import app


async def _request(path: str) -> httpx.Response:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.get(path)


def test_health_returns_public_runtime_state() -> None:
    response = asyncio.run(_request("/health"))

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "analysis-api",
        "version": "0.1.0",
        "environment": "development",
        "demo_mode": True,
    }


def test_openapi_contains_health_endpoint() -> None:
    schema = app.openapi()

    assert "/health" in schema["paths"]
    assert schema["info"]["title"] == "Lattice CT Analysis API"
