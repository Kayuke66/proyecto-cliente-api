import json
from typing import Any

from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import JSONResponse

from src.schemas.digital_twin import SiteNodeDto, DeviceDto, PointDto
from src.schemas.imports import (
    ImportEdeResponseDto,
    ImportSantraLegacyResponseDto,
    SantraLegacyJson,
    SaveDigitalTwinResponseDto,
    LoadDigitalTwinResponseDto
)
from src.services.digital_twin_service import DigitalTwinService
from src.services.digital_twin_store import digital_twin
from src.services.persistence_service import PersistenceService
from src.core.errors.catalog import ERRORS
from src.core.errors.model import SantraError
router = APIRouter()

persistence = PersistenceService()
persistence.init()

service = DigitalTwinService(digital_twin, persistence)
service.init()


@router.post(
    "/api/digital-twin/import/ede",
    tags=["Digital-Twin"],
    summary="Import Digital Twin model from EDE file content",
    responses={
        200: {
            "description": "EDE successfully imported",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "siteId": {"type": "string"},
                            "devices": {"type": "integer"},
                            "points": {"type": "integer"},
                            "structureSource": {
                                "anyOf": [
                                    {"type": "object"},
                                    {"type": "null"}
                                ]
                            },
                        },
                        "required": ["siteId", "devices", "points"],
                    },
                    "example": {
                        "siteId": "default",
                        "devices": 0,
                        "points": 0,
                        "structureSource": None,
                    }
                }
            },
        },
        400: {
            "description": "Invalid input",
        },
    },
)
async def import_ede(
    content: str = Body(
        ...,
        media_type="text/plain",
        example="B_01'STecnica'Box1...;\nB_01'STecnica'...",
    )
):
    if not content or not isinstance(content, str) or len(content.strip()) == 0:
        err = ERRORS["IMPORT_EDE_VALIDATION_FAILED"]
        raise SantraError(
            code=err["code"],
            message="Invalid EDE content",
            category=err["category"],
            module="digital_twin.controller.importEde",
            meta={"details": ["Invalid EDE content"]},
            status_code=400,
        )

    result = service.import_ede(content)

    if result.get("errors"):
        err = ERRORS["IMPORT_EDE_VALIDATION_FAILED"]
        raise SantraError(
            code=err["code"],
            message=err["message"],
            category=err["category"],
            module="digital_twin.controller.importEde",
            meta={"details": result["errors"]},
            status_code=400,
        )

    return {
        "siteId": result["siteId"],
        "devices": result["devices"],
        "points": result["points"],
        "structureSource": result.get("structureStats"),
    }

@router.post(
    "/api/digital-twin/import/santra-legacy-json",
    tags=["Digital-Twin"],
    summary="Import Santra Legacy JSON",
    response_model=ImportSantraLegacyResponseDto,
    responses={
        200: {
            "description": "Import successful",
            "content": {
                "application/json": {
                    "example": {
                        "siteId": "TESTSITE",
                        "devices": 10,
                        "points": 250,
                    }
                }
            },
        },
        400: {
            "description": "Invalid input",
        },
        500: {
            "description": "Import failed",
        }
    },
)
async def import_santra_legacy_json(
    content: dict[str, Any] = Body(
        ...,
        media_type="application/json",
        example={
            "idPlanta": "TESTSITE",
            "denominacion": "Test Site",
            "legalEntity": "B88888888",
            "language": "fr",
            "dispositivos": [
                {
                    "device_id": "string",
                    "device_name": "string",
                    "protocolo": "string",
                    "host": "string",
                    "puntos": [
                        {
                            "add": "5-20",
                            "shortName": "string",
                            "desc": "string",
                            "escala": 0,
                            "desplazamiento": 0,
                            "digital": True,
                            "unidad": "string",
                            "write": True,
                            "area": "string"
                        }
                    ]
                }
            ],
            "deltas": [
                {
                    "add": "string",
                    "punto": {
                        "add": "5-20",
                        "shortName": "string",
                        "desc": "string",
                        "escala": 0,
                        "desplazamiento": 0,
                        "digital": True,
                        "unidad": "string",
                        "write": True,
                        "area": "string"
                    }
                }
            ],
            "calculados": [
                {
                    "add": "string",
                    "desc": "string",
                    "area": "string",
                    "unidad": "string",
                    "escala": 0,
                    "datos": [
                        {
                            "device_id": 0,
                            "add": "string",
                            "valor": 0,
                            "operacion": "string"
                        }
                    ]
                }
            ]
        }
    )
):
    if not content or not isinstance(content, dict):
        err = ERRORS["SANTRA_LEGACY_JSON_INVALID"]
        raise SantraError(
            code=err["code"],
            message=err["message"],
            category=err["category"],
            module="digital_twin.controller.importSantraLegacyJson",
            status_code=400,
        )

    result = service.import_santra_legacy_json(json.dumps(content))

    return ImportSantraLegacyResponseDto(
        siteId=result["siteId"],
        devices=result["devices"],
        points=result["points"],
    )


@router.get(
    "/api/digital-twin/tree",
    tags=["Digital-Twin"],
    summary="Get hierarchical Digital Twin tree",
    response_model=dict[str, SiteNodeDto],
    response_model_exclude_none=True,
    responses={
        200: {
            "description": "Hierarchical Digital Twin model",
            "content": None
        }
    },
)
async def get_hierachical_digital_twin_tree():
    return service.get_tree()


@router.get(
    "/api/digital-twin/devices",
    tags=["Digital-Twin"],
    summary="Get all devices",
    response_model=list[DeviceDto],
    responses={
        200: {
            "description": "List of devices",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "string",
                            "name": "string",
                            "description": "string",
                            "protocol": "string",
                            "vendor": "string",
                            "model": "string",
                        }
                    ]
                }
            },
        }
    },
)
async def get_all_devices():
    return service.get_devices()


@router.get(
    "/api/digital-twin/devices/{id}",
    tags=["Digital-Twin"],
    summary="Get device by ID",
    response_model=DeviceDto,
    responses={
        200: {
            "description": "Device found",
            "content": None
        },
        404: {
            "description": "Device not found",
            "content": None
        },
    },
)
async def get_device_by_id(id: str):
    device = service.get_device(id)

    if not device:
        err = ERRORS["DEVICE_NOT_FOUND"]
        raise SantraError(
            code=err["code"],
            message=err["message"],
            category=err["category"],
            module="digital_twin.route.get_device_by_id",
            meta={"deviceId": id},
            status_code=404,
        )

    return device


@router.get(
    "/api/digital-twin/devices/{id}/points",
    tags=["Digital-Twin"],
    summary="Get all points for a device",
    response_model=list[PointDto],
    responses={
        200: {
            "description": "Points of the device",
            "content":{
                "application/json": {
                    "example": [
                        {
                            "id": "string",
                            "name": "string",
                            "deviceId": "string",
                            "metric": "string",
                            "objectType": "string",
                            "objectInstance": "string",
                            "type": "string",
                            "writable": True,
                            "unit": "string",
                            "description": "string",
                        }
                    ]
                }
            },
        },
        404: {
            "description": "Device not found",
            "content": None,
        },
    },
)
async def get_points_by_device(id: str):
    device = service.get_device(id)

    if not device:
        err = ERRORS["DEVICE_NOT_FOUND"]
        raise SantraError(
            code=err["code"],
            message=err["message"],
            category=err["category"],
            module="digital_twin.route.get_points_by_device",
            meta={"deviceId": id},
            status_code=404,
        )

    return service.get_points_by_device(id)


@router.get(
    "/api/digital-twin/equipments/{id}/points",
    tags=["Digital-Twin"],
    summary="Get all points for an equipment",
    description="Returns all points associated with a given equipment. "
                "If the equipment has no points or does not exist, an empty array is returned.",
    response_model=list[PointDto],
    responses={
        200: {
            "description": "Points of the equipment",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "string",
                            "name": "string",
                            "deviceId": "string",
                            "metric": "string",
                            "objectType": "string",
                            "objectInstance": "string",
                            "type": "string",
                            "writable": True,
                            "unit": "string",
                            "description": "string",
                        }
                    ]
                }
            },
        },
    },
)
async def get_points_by_equipment(id: str):
    return service.get_points_by_equipment(id)


@router.get(
    "/api/digital-twin/points",
    tags=["Digital-Twin"],
    summary="Get all points",
    response_model=list[PointDto],
    responses={
        200: {
            "description": "List of all points",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "string",
                            "name": "string",
                            "deviceId": "string",
                            "metric": "string",
                            "objectType": "string",
                            "objectInstance": "string",
                            "type": "string",
                            "writable": True,
                            "unit": "string",
                            "description": "string",
                        }
                    ]
                }
            },
        },
    },
)
async def get_all_points():
    return service.get_points()


@router.post(
    "/api/digital-twin/save",
    tags=["Digital-Twin"],
    summary="Save current Digital Twin model",
    description="Persists the current in-memory Digital Twin snapshot.",
    status_code=status.HTTP_201_CREATED,
    response_model=SaveDigitalTwinResponseDto,
    responses={
        201: {
            "description": "Model saved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ok"
                    }
                }
            },
        },
    },
)
async def save_digital_twin():
    service.save()
    return SaveDigitalTwinResponseDto(status="ok")

@router.post(
    "/api/digital-twin/load",
    tags=["Digital-Twin"],
    summary="Load Digital Twin from persistence",
    status_code=status.HTTP_200_OK,
    response_model=LoadDigitalTwinResponseDto,
    responses={
        200: {
            "description": "Model loaded successfully",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ok"
                    }
                }
            },
        },
    },
)
async def load_digital_twin():
    service.load()
    return LoadDigitalTwinResponseDto(status="ok")