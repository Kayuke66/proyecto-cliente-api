import hashlib

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import Response as FastAPIResponse
from starlette.responses import Response as StarletteResponse

from src.api.routes.digital_twin import router as digital_twin_router
from src.api.routes.health import router as health_router
from src.api.routes.system import router as system_router

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


app = FastAPI(
    title="Santra API Client - Nomia Energy",
    description="Python API Client for Santra Edge Agent",
    openapi_tags=tags_metadata,
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="0.1.0",
        description=app.description,
        routes=app.routes,
        tags=tags_metadata,
    )

    schemas = openapi_schema.get("components", {}).get("schemas", {})
    schemas.pop("HealthCheckResult", None)
    schemas.pop("HealthResponseDto", None)
    schemas.pop("VersionResponseDto", None)

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=[
        "ETag",
        "RateLimit-Limit",
        "RateLimit-Policy",
        "RateLimit-Remaining",
        "RateLimit-Reset",
        "Vary",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Methods",
        "Access-Control-Allow-Headers",
    ],
)


@app.middleware("http")
async def add_common_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"

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


app.include_router(health_router)
app.include_router(system_router)
app.include_router(digital_twin_router)
