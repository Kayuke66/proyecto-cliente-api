from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class ImportEdeResponseDto(BaseModel):
    model_config = ConfigDict(title="ImportEdeResponse")

    siteId: str
    devices: int
    points: int
    structureSource: Any | None = None

class ImportSantraLegacyResponseDto(BaseModel):
    model_config = ConfigDict(title="ImportSantraLegacyResponse")

    siteId: str = Field(..., example= "TESTSITE")
    devices: int = Field(..., example= 10)
    points: int = Field(..., example= 250)


class SantraLegacyPoint(BaseModel):
    model_config = ConfigDict(title="SantraLegacyPoint")

    add: str = Field(..., example= "5-20")
    shortName: str
    desc: str
    escala: float
    desplazamiento: float
    digital: bool
    unidad: str
    write: bool
    area: str


class SantraLegacyDevice(BaseModel):
    model_config = ConfigDict(title="SantraLegacyDevice")

    device_id: str | float
    device_name: str
    protocolo: str
    host: str
    puntos: list[SantraLegacyPoint] = Field(default_factory=list)


class SantraLegacyDelta(BaseModel):
    model_config = ConfigDict(title="SantraLegacyDelta")

    add: str
    punto: SantraLegacyPoint = Field(default_factory=list)


class SantraLegacyCalculated(BaseModel):
    add: str
    desc: str
    area: str
    unidad: str
    escala: float
    datos: list[dict[str, Any]] = Field(
        ...,
        json_schema_extra={
            "items": {
                "type": "object",
                "properties": {
                    "device_id": {
                        "oneOf": [
                            {"type": "number"},
                            {"type": "string"},
                            {"type": "null"},
                        ]
                    },
                    "add": {"type": "string"},
                    "valor": {"type": "number"},
                    "operacion": {"type": "string"},
                },
                "required": ["operacion"],
            }
        },
    )


class SantraLegacyJson(BaseModel):
    model_config = ConfigDict(title="SantraLegacyJson")

    idPlanta: str = Field(..., example="TESTSITE")
    denominacion: str = Field(..., example="Test Site")
    legalEntity: str = Field(..., example="B88888888")
    language: str = Field(example="fr")
    dispositivos: list[SantraLegacyDevice] = Field(default_factory=list)
    deltas: list[SantraLegacyDelta] = Field(default_factory=list)
    calculados: list[SantraLegacyCalculated] = Field(default_factory=list)