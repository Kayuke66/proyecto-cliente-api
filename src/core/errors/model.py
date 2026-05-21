from typing import Any


class SantraError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        category: str,
        module: str | None = None,
        meta: dict[str, Any] | None = None,
        status_code: int = 400,
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.category = category
        self.module = module
        self.meta = meta
        self.status_code = status_code