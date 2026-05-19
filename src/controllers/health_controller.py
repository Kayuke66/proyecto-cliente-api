from src.services.health_monitor.health_monitor_service import HealthMonitorService


class HealthController:
    def __init__(self, health_monitor: HealthMonitorService):
        self.health_monitor = health_monitor

    async def get_health(self):
        return await self.health_monitor.run_checks()