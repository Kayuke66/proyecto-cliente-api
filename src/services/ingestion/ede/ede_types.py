from pydantic import BaseModel
from typing import Literal


class EdeMetadata(BaseModel):
    projectName: str


class EdeRow(BaseModel):
    keyname: str
    deviceId: str
    objectName: str
    objectType: str
    objectInstance: str
    description: str | None = None
    unit: str | None = None
    stateText: list[str] | None = None


class EdeParsed(BaseModel):
    metadata: EdeMetadata
    rows: list[EdeRow]


class StructureSourceStats(BaseModel):
    keyname: int
    objectName: int


class ResolvedHierarchy(BaseModel):
    buildingId: str
    floorId: str
    roomId: str
    equipmentId: str


class ResolvedStructure(BaseModel):
    source: Literal["keyname", "objectName"]
    hierarchy: ResolvedHierarchy
    metric: str