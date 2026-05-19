import time
from src.schemas.health import HealthResponseDto, HealthCheckResult


class HealthMonitorService:
    def __init__(self, checks: list):
        self.checks = checks

    async def run_checks(self) -> HealthResponseDto:
        results: dict[str, HealthCheckResult] = {}

        for check in self.checks:
            try:
                result = await check.run()
                results[check.name] = result
            except Exception as error:
                results[check.name] = HealthCheckResult(
                    status="error",
                    message="Check execution failed",
                    timestamp=int(time.time() * 1000),
                    meta={"error": str(error)},
                )

        return HealthResponseDto(
            status=self._aggregate_status(results),
            timestamp=int(time.time() * 1000),
            checks=results,
        )

    def _aggregate_status(self, results: dict[str, HealthCheckResult]) -> str:
        has_warning = False

        for result in results.values():
            if result.status == "error":
                return "error"
            if result.status == "warning":
                has_warning = True

        return "warning" if has_warning else "ok"