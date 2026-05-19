from fastapi import APIRouter
from src.schemas.digital_twin import SiteNodeDto, DeviceDto
from src.services.digital_twin_service import DigitalTwinService
from src.services.digital_twin_store import digital_twin

router = APIRouter()

service = DigitalTwinService(digital_twin)


@router.get(
    "/api/digital-twin/tree",
    tags=["Digital-Twin"],
    summary="Get hierarchical Digital Twin tree",
    response_model=dict[str, SiteNodeDto],
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
        }
    }
)
async def get_all_devices():
    return service.get_devices()