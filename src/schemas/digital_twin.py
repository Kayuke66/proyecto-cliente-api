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
    deviceId: str
    metric: str
    objectType: str
    objectInstance: str
    type: str
    writable: bool
    unit: str
    description: str

    bacnetType: dict[str, str] | None = Field(default=None, repr=False, exclude=True)
    scale: float | None = Field(default=None, repr=False, exclude=True)
    offset: float | None = Field(default=None, repr=False, exclude=True)
    source: str | None = Field(default=None, repr=False, exclude=True)
    expression: list[dict[str, Any]] | None = Field(default=None, repr=False, exclude=True)
    dependencies: list[str] | None = Field(default=None, repr=False, exclude=True)
    metadata: dict[str, Any] | None = Field(default=None, repr=False, exclude=True)

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