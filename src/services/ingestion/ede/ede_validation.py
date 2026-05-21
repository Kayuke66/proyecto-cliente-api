from src.services.ingestion.ede.ede_types import EdeParsed


class EdeValidator:
    def validate(self, parsed: EdeParsed):
        errors: list[str] = []

        has_device = any(row.objectType == "8" for row in parsed.rows)
        if not has_device:
            errors.append("EDE does not contain any device definition (object-type = 8)")

        for row in parsed.rows:
            if not row.deviceId:
                errors.append(f"Row with object {row.objectName} has no deviceId")

        return {
            "isValid": len(errors) == 0,
            "errors": errors,
        }