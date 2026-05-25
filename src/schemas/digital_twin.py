from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class DeviceDto(BaseModel):
    id: str
    name: str
    description: str | None = None
    protocol: str | None = None
    host: str | None = None
    port: int | None = None
    unitId: int = 0


class PointDto(BaseModel):
    model_config = ConfigDict(title="Point")

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
    offset: float | int
    source: str

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