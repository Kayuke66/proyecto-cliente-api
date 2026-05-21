from typing import Any
from src.core.errors.catalog import ERRORS


def build_error(
    key: str,
    details: list[str] | None = None,
    message: str | None = None,
    meta: dict[str, Any] | None = None,
):
    err = ERRORS[key]

    payload = {
        "error": {
            "code": err["code"],
            "message": message or err["message"],
            "category": err["category"],
        }
    }

    if meta is not None:
        payload["error"]["details"] = meta
    elif details is not None:
        payload["error"]["details"] = {"details": details}

    return payload