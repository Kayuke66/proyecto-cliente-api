import time
from src.schemas.health import HealthCheckResult

PROCESS_START_TIME = time.time()


class UptimeCheck:
    name = "uptime"

    async def run(self) -> HealthCheckResult:
        uptime = time.time() - PROCESS_START_TIME
        timestamp = int(time.time() * 1000)

        seconds = int(uptime)
        hours = round(uptime / 3600, 2)
        days = round(uptime / 86400, 2)

        status = "warning" if days > 30 else "ok"
        started_at = time.strftime(
            "%d/%m/%Y %H:%M",
            time.localtime((timestamp / 1000) - seconds)
        )

        return HealthCheckResult(
            status=status,
            timestamp=timestamp,
            meta={
                "uptimeSeconds": seconds,
                "uptimeHours": round(hours, 2),
                "uptimeDays": round(days, 2),
                "uptimeFormatted": self._format_uptime(seconds),
                "startedAt": started_at,
            },
        )

    def _format_uptime(self, seconds: int) -> str:
        d = seconds // 86400
        h = (seconds % 86400) // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{d}d {h}h {m}m {s}s"