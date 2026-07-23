"""Process health endpoint with no external dependencies."""

from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.health import HealthResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Report liveness and non-secret runtime mode."""
    settings = get_settings()
    return HealthResponse(
        status="ok",
        service="analysis-api",
        version="0.1.0",
        environment=settings.app_env,
        demo_mode=settings.demo_mode,
    )
