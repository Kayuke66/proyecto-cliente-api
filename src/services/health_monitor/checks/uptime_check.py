import time
from src.schemas.health import HealthCheckResult


PROCESS_START_TIME = time.time()


class UptimeCheck:
    name = "uptime"

    async def run(self) -> HealthCheckResult:
        now_ms = int(time.time() * 1000)
        uptime_seconds = int(time.time() - PROCESS_START_TIME)

        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60
        seconds = uptime_seconds % 60

        return HealthCheckResult(
            status="ok",
            message="",
            timestamp=now_ms,
            meta={
                "uptimeSeconds": uptime_seconds,
                "uptimeHours": round(uptime_seconds / 3600, 2),
                "uptimeFormatted": f"{days}d {hours}h {minutes}m {seconds}s",
                "startedAt": time.strftime("%d/%m/%Y %H:%M", time.localtime(PROCESS_START_TIME)),
            },
        )