from typing import Any
from pydantic import BaseModel


class DeviceDto(BaseModel):
    id: str
    name: str
    description: str | None = None
    protocol: str | None = None
    vendor: str | None = None
    model: str | None = None


class PointDto(BaseModel):
    id: str
    name: str
    description: str
    deviceId: str
    metric: str
    objectType: str
    objectInstance: str
    bacnetType: dict[str, str] | None = None
    type: str
    writable: bool
    unit: str
    stateText: list[str] | None = None
    scale: float | None = None
    offset: float | None = None
    source: str | None = None
    expression: list[dict[str, Any]] | None = None
    dependencies: list[str] | None = None
    metadata: dict[str, Any] | None = None


class CompactPointDto(BaseModel):
    id: str
    name: str
    description: str
    deviceId: str
    type: str


class BaseNodeDto(BaseModel):
    id: str
    name: str
    description: str | None = None
    metadata: dict[str, Any] | None = None


class EquipmentNodeDto(BaseNodeDto):
    points: list[CompactPointDto]


class RoomNodeDto(BaseNodeDto):
    equipments: dict[str, "EquipmentNodeDto"]


class FloorNodeDto(BaseNodeDto):
    rooms: dict[str, "RoomNodeDto"]


class BuildingNodeDto(BaseNodeDto):
    floors: dict[str, "FloorNodeDto"]


class SiteNodeDto(BaseNodeDto):
    buildings: dict[str, "BuildingNodeDto"]

EquipmentNodeDto.model_rebuild()
RoomNodeDto.model_rebuild()
FloorNodeDto.model_rebuild()
BuildingNodeDto.model_rebuild()
SiteNodeDto.model_rebuild()