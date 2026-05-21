from typing import Protocol, Any, Callable


class ImportContext(dict):
    siteId: str
    buildingId: str
    siteName: str
    buildingName: str
    siteMetadata: dict[str, Any]
    buildingMetadata: dict[str, Any]
    areasMap: dict[str, Any]
    buildHierarchy: Callable[[str, str], dict]
    normalizeMetric: Callable[[str], str]


class ProtocolIngestionStrategy(Protocol):
    def import_device(self, device: dict, context: dict, twin_service) -> None:
        ...