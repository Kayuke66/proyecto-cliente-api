import asyncio
import time
from src.schemas.health import HealthCheckResult


class EventLoopCheck:
    name = "event_loop"

    def __init__(self, warning_ms: int = 150, error_ms: int = 500):
        self.warning_ms = warning_ms
        self.error_ms = error_ms

    async def run(self) -> HealthCheckResult:
        start = time.perf_counter()
        await asyncio.sleep(0)
        delay_ms = (time.perf_counter() - start) * 1000
        now_ms = int(time.time() * 1000)

        if delay_ms >= self.error_ms:
            status = "error"
        elif delay_ms >= self.warning_ms:
            status = "warning"
        else:
            status = "ok"

        return HealthCheckResult(
            status=status,
            message="",
            timestamp=now_ms,
            meta={
                "delayMs": round(delay_ms, 2),
            },
        )