from typing import Literal, TypedDict

ErrorCategory = Literal["error", "warning", "info"]


class ErrorDef(TypedDict):
    code: str
    message: str
    category: ErrorCategory


ERRORS: dict[str, ErrorDef] = {
    "UNHANDLED_EXCEPTION": {
        "code": "ERR_SMA_001",
        "message": "Unhandled Exception",
        "category": "error",
    },
    "SERVER_CYCLE_BLOCK": {
        "code": "ERR_SMA_002",
        "message": "Event loop delay detected",
        "category": "warning",
    },
    "SERVER_ROUTE_ERROR": {
        "code": "ERR_SMA_003",
        "message": "The requested route is not available",
        "category": "error",
    },
    "HEALTH_MONITOR_ERROR": {
        "code": "ERR_SMA_004",
        "message": "Health monitor check failed",
        "category": "error",
    },
    "HEALTH_CHECK_WARNING": {
        "code": "ERR_SMA_005",
        "message": "Health check warning - Issue detected",
        "category": "warning",
    },
    "DEVICE_NOT_FOUND": {
        "code": "ERR_SMA_008",
        "message": "Device not found",
        "category": "error",
    },
    "UNHANDLED_REJECTION": {
        "code": "ERR_SMA_006",
        "message": "Unhandled Promise Rejection",
        "category": "error",
    },
    "IMPORT_EDE_VALIDATION_FAILED": {
        "code": "ERR_SMA_007",
        "message": "EDE file validation failed",
        "category": "error",
    },
}