"""System endpoint schemas."""

from typing import Literal

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """Public liveness information safe for frontend display."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ok"]
    service: Literal["analysis-api"]
    version: str
    environment: str
    demo_mode: bool
