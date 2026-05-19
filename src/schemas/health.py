from typing import Literal, Any
from pydantic import BaseModel

HealthStatus = Literal["ok", "warning", "error"]


class HealthCheckResult(BaseModel):
    status: HealthStatus
    message: str
    timestamp: int
    meta: dict[str, Any]


class HealthResponseDto(BaseModel):
    status: HealthStatus
    timestamp: int
    checks: dict[str, HealthCheckResult]