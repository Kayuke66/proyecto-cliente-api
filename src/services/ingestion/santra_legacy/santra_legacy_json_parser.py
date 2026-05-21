import json

from src.core.errors.catalog import ERRORS
from src.core.errors.model import SantraError


class SantraLegacyJsonParser:
    def parse(self, content: str):
        try:
            return json.loads(content)
        except Exception as error:
            err = ERRORS["SANTRA_LEGACY_JSON_INVALID"]
            raise SantraError(
                code=err["code"],
                message=err["message"],
                category=err["category"],
                module="santra_legacy_json.parser",
                meta={"originalError": str(error)},
                status_code=400,
            )