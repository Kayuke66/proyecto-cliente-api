import hashlib

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import Response as FastAPIResponse
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.responses import Response as StarletteResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager

from src.schemas.imports import (
    SantraLegacyJson,
    SantraLegacyDevice,
    SantraLegacyPoint,
    SantraLegacyDelta,
    SantraLegacyCalculated,
)
from src.core.errors.factory import build_error
from src.api.routes.digital_twin import router as digital_twin_router, persistence, service
from src.api.routes.health import router as health_router
from src.api.routes.system import router as system_router
from src.core.errors.model import SantraError

tags_metadata = [
    {
        "name": "Health",
        "description": "Health monitoring endpoints",
    },
    {
        "name": "System",
        "description": "System information endpoints",
    },
    {
        "name": "Digital-Twin",
        "description": "Digital Twin management",
    },
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    persistence.init()
    service.init()
    yield
app = FastAPI(
    title="Santra API Client - Nomia Energy",
    description="Python API Client for Santra Edge Agent",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=app.description,
        routes=app.routes,
        tags=tags_metadata,
    )

    for path_item in openapi_schema.get("paths", {}).values():
        for operation in path_item.values():
            if not isinstance(operation, dict):
                continue
            operation.get("responses", {}).pop("422", None)

    schemas = openapi_schema.get("components", {}).get("schemas", {})
    schemas.setdefault("SantraLegacyPoint", SantraLegacyPoint.model_json_schema())
    schemas.setdefault("SantraLegacyDevice", SantraLegacyDevice.model_json_schema())
    schemas.setdefault("SantraLegacyDelta", SantraLegacyDelta.model_json_schema())
    schemas.setdefault("SantraLegacyCalculated", SantraLegacyCalculated.model_json_schema())
    schemas.setdefault("SantraLegacyJson", SantraLegacyJson.model_json_schema())
    schemas.pop("HealthCheckResult", None)
    schemas.pop("HealthResponseDto", None)
    schemas.pop("VersionResponseDto", None)
    schemas.pop("HTTPValidationError", None)
    schemas.pop("ValidationError", None)
    schemas.pop("BuildingNodeDto", None)
    schemas.pop("CompactPointDto", None)
    schemas.pop("SiteNodeDto", None)
    schemas.pop("RoomNodeDto", None)
    schemas.pop("EquipmentNodeDto", None)
    schemas.pop("FloorNodeDto", None)


    desired_order = [
        "PointDto",
        "SantraLegacyJson",
        "SantraLegacyDevice",
        "SantraLegacyPoint",
        "SantraLegacyDelta",
        "SantraLegacyCalculated",
        "ImportSantraLegacyResponse",
    ]
    ordered_schemas = {}
    for schema_name in desired_order:
        if schema_name in schemas:
            ordered_schemas[schema_name] = schemas.pop(schema_name)

    ordered_schemas.update(schemas)

    openapi_schema["components"]["schemas"] = ordered_schemas

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.middleware("http")
async def add_common_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"

    response.headers["Connection"] = "keep-alive"
    response.headers["Keep-Alive"] = "timeout=5"

    response.headers["RateLimit-Limit"] = "50"
    response.headers["RateLimit-Policy"] = "50;w=1"
    response.headers["RateLimit-Remaining"] = "49"
    response.headers["RateLimit-Reset"] = "1"

    response.headers["Vary"] = "Accept-Encoding"

    body = b""
    async for chunk in response.body_iterator:
        body += chunk

    if body:
        etag = hashlib.md5(body).hexdigest()
        response.headers["ETag"] = f"\"{etag}\""

    return StarletteResponse(
        content=body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first = exc.errors()[0] if exc.errors() else {}
    loc = first.get("loc", [])
    msg = first.get("msg", "Invalid input")
    field_name = ".".join(str(x) for x in loc[1:]) if len(loc) > 1 else ""
    final_msg = f"{field_name}: {msg}" if field_name else msg

    return JSONResponse(
        status_code=400,
        content=build_error(
            "IMPORT_EDE_VALIDATION_FAILED",
            details=[final_msg],
        ),
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content=build_error("SERVER_ROUTE_ERROR"),
        )

    return JSONResponse(
        status_code=exc.status_code,
        content=build_error(
            "UNHANDLED_EXCEPTION",
            details=[str(exc.detail)] if exc.detail else None,
        ),
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=build_error(
            "UNHANDLED_EXCEPTION",
            details=[str(exc)],
        ),
    )


@app.exception_handler(SantraError)
async def santra_error_handler(request: Request, exc: SantraError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "category": exc.category,
                "details": exc.meta,
            }
        },
    )


@app.exception_handler(SantraError)
async def santra_exception_handler(request: Request, exc: SantraError):
    content = {
        "error": {
            "code": exc.code,
            "message": exc.message,
            "category": exc.category,
        }
    }

    if exc.meta is not None:
        content["error"]["details"] = exc.meta

    return JSONResponse(
        status_code=exc.status_code,
        content=content,
    )


app.include_router(health_router)
app.include_router(system_router)
app.include_router(digital_twin_router)
