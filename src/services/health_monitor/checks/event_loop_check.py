import asyncio
import time
from src.schemas.health import HealthCheckResult


class EventLoopCheck:
    name = "event_loop"

    def __init__(self, interval_ms: int = 0, max_delay_ms: int = 150):
        self.interval_ms = interval_ms
        self.max_delay_ms = max_delay_ms

    async def run(self) -> HealthCheckResult:
        start = time.perf_counter()

        await asyncio.sleep(self.interval_ms / 1000)

        delay_ms = (time.perf_counter() - start) * 1000
        timestamp = int(time.time() * 1000)

        if delay_ms > self.max_delay_ms:
            return HealthCheckResult(
                status="warning",
                message="Event loop delay detected",
                timestamp=timestamp,
                meta={
                    "delayMs": round(delay_ms, 2),
                    "thresholdMs": self.max_delay_ms,
                },
            )

        return HealthCheckResult(
            status="ok",
            timestamp=timestamp,
            meta={
                "delayMs": round(delay_ms, 2),
            },
        )