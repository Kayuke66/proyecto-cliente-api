from typing import Any, Literal
from pydantic import BaseModel, ConfigDict

HealthStatus = Literal["ok", "warning", "error"]


class HealthCheckResult(BaseModel):
    status: HealthStatus
    message: str | None = None
    timestamp: int
    meta: dict[str, Any] | None = None

class HealthResponseDto(BaseModel):
    status: HealthStatus
    timestamp: int
    checks: dict[str, HealthCheckResult]