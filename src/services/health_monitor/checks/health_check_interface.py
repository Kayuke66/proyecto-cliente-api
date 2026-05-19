from abc import ABC, abstractmethod
from src.schemas.health import HealthCheckResult


class HealthCheck(ABC):
    name: str

    @abstractmethod
    async def run(self) -> HealthCheckResult:
        pass