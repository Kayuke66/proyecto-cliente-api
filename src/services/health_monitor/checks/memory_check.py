import time
import psutil
from src.schemas.health import HealthCheckResult


class MemoryCheck:
    name = "memory"

    def __init__(self, warning_mb: int, error_mb: int):
        self.warning_mb = warning_mb
        self.error_mb = error_mb

    async def run(self) -> HealthCheckResult:
        process = psutil.Process()
        memory_mb = process.memory_info().rss / 1024 / 1024
        now_ms = int(time.time() * 1000)
        print(self.warning_mb)
        if memory_mb >= self.error_mb:
            status = "error"
        elif memory_mb >= self.warning_mb:
            status = "warning"
        else:
            status = "ok"

        return HealthCheckResult(
            status=status,
            message="",
            timestamp=now_ms,
            meta={
                "heapUsedMb": round(memory_mb, 2),
                "heapTotalMb": round(memory_mb, 2),
                "rssMb": round(memory_mb, 2),
            },
        )