from typing import Any
from pydantic import BaseModel, ConfigDict


class ImportEdeResponseDto(BaseModel):
    model_config = ConfigDict(title="ImportEdeResponse")

    siteId: str
    devices: int
    points: int
    structureSource: Any | None = None

class ImportSantraLegacyResponseDto(BaseModel):
    model_config = ConfigDict(title="ImportSantraLegacyResponse")

    siteId: str
    devices: int
    points: int