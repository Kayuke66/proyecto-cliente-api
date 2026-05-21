import time
import psutil
import tracemalloc
from src.schemas.health import HealthCheckResult

if not tracemalloc.is_tracing():
    tracemalloc.start()


class MemoryCheck:
    name = "memory"

    def __init__(self, max_heap_used_mb_warning: int = 250, max_heap_used_mb_error: int = 500):
        self.max_heap_used_mb_warning = max_heap_used_mb_warning
        self.max_heap_used_mb_error = max_heap_used_mb_error

    async def run(self) -> HealthCheckResult:
        process = psutil.Process()
        mem_info = process.memory_info()

        current, peak = tracemalloc.get_traced_memory()

        heap_used_mb = current / 1024 / 1024
        heap_total_mb = peak / 1024 / 1024
        rss_mb = mem_info.rss / 1024 / 1024

        try:
            full_info = process.memory_full_info()
            external_bytes = getattr(full_info, "data", 0)
        except Exception:
            external_bytes = 0

        external_mb = external_bytes / 1024 / 1024

        timestamp = int(time.time() * 1000)
        status = "ok"

        if heap_used_mb > self.max_heap_used_mb_error:
            status = "error"
        elif heap_used_mb > self.max_heap_used_mb_warning:
            status = "warning"

        meta = {
            "heapUsedMb": round(heap_used_mb, 2),
            "heapTotalMb": round(heap_total_mb, 2),
            "rssMb": round(rss_mb, 2),
            "externalMb": round(external_mb, 2),
            "thresholdMbWarning": self.max_heap_used_mb_warning,
            "thresholdMbError": self.max_heap_used_mb_error,
        }

        if status != "ok":
            return HealthCheckResult(
                status=status,
                message="High memory usage detected",
                timestamp=timestamp,
                meta=meta,
            )

        return HealthCheckResult(
            status="ok",
            timestamp=timestamp,
            meta=meta,
        )