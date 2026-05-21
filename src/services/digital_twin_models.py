from dataclasses import dataclass, field
from typing import Any


@dataclass
class Device:
    id: str
    name: str
    description: str | None = None
    protocol: str | None = None
    vendor: str | None = None
    model: str | None = None
    host: str | None = None
    port: int | None = None
    unitId: int | None = None
    metadata: dict[str, Any] | None = None


@dataclass
class Point:
    id: str
    name: str
    deviceId: str
    metric: str
    objectType: str
    objectInstance: str
    type: str
    writable: bool
    description: str | None = None
    unit: str | None = None
    bacnetType: dict[str, str] | None = None
    stateText: list[str] | None = None
    scale: float | None = None
    offset: float | None = None
    source: str | None = None
    expression: list[dict[str, Any]] | None = None
    dependencies: list[str] | None = None
    metadata: dict[str, Any] | None = None
    equipmentId: str | None = None