from fastapi import APIRouter
from src.schemas.system import VersionResponseDto
from src.services.system_service import get_version

router = APIRouter()


@router.get(
    "/api/version",
    tags=["System"],
    summary="Get service current version",
    response_model=VersionResponseDto,
    responses={
        200: {
            "description": "Edge Agent Version",
            "content": None
        }
    },
)
async def get_service_current_version():
    return get_version()