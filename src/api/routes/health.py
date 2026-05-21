from fastapi import APIRouter
from src.controllers.health_controller import HealthController
from src.schemas.health import HealthResponseDto
from src.services.health_monitor.health_monitor_service import HealthMonitorService
from src.services.health_monitor.checks.event_loop_check import EventLoopCheck
from src.services.health_monitor.checks.uptime_check import UptimeCheck
from src.services.health_monitor.checks.memory_check import MemoryCheck

router = APIRouter()

health_monitor = HealthMonitorService([
    EventLoopCheck(0, 150),
    UptimeCheck(),
    MemoryCheck(250, 500),
])

controller = HealthController(health_monitor)


@router.get(
    "/api/health",
    tags=["Health"],
    summary="Get agent health status",
    response_model=HealthResponseDto,
    response_model_exclude_none=True,
    responses={
        200: {
            "description": "Health status",
            "content": None
        }
    },
)
async def get_agent_health_status():
    return await controller.get_health()