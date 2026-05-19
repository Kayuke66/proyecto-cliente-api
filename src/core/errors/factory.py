from src.core.errors.catalog import ERRORS


def build_error(key: str, details: list[str] | None = None, message: str | None = None):
    err = ERRORS[key]
    payload = {
        "error": {
            "code": err["code"],
            "message": message or err["message"],
            "category": err["category"],
        }
    }

    if details is not None:
        payload["error"]["details"] = {"details": details}

    return payload