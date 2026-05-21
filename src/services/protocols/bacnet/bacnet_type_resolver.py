from src.services.protocols.bacnet.bacnet_type_catalog import BACNET_OBJECT_TYPES


class BacnetTypeResolver:
    def resolve(self, object_type: str) -> dict:
        try:
            type_number = int(object_type)
        except (TypeError, ValueError):
            return {
                "name": "unknown",
                "category": "unknown",
            }

        return BACNET_OBJECT_TYPES.get(
            type_number,
            {
                "name": f"unknown_{type_number}",
                "category": "unknown",
            },
        )