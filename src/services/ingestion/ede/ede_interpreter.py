from src.services.ingestion.ede.ede_types import EdeParsed, EdeRow
from src.services.ingestion.ede.structure_resolver import StructureResolver
from src.services.ingestion.hierarchy_builder import HierarchyBuilder
from src.services.protocols.bacnet.bacnet_type_resolver import BacnetTypeResolver


class EdeInterpreter:
    def __init__(self, twin_service):
        self.twin_service = twin_service
        self.structure_resolver = StructureResolver()
        self.hierarchy_builder = HierarchyBuilder()
        self.warnings: list[str] = []
        self.structure_stats = {
            "keyname": 0,
            "objectName": 0,
        }
        self.bacnet_type_resolver = BacnetTypeResolver()

    def import_data(self, parsed: EdeParsed) -> None:
        site_id = parsed.metadata.projectName or "default"

        for row in parsed.rows:
            if self._is_device(row):
                self.twin_service.create_device({
                    "id": row.deviceId,
                    "name": row.objectName or row.deviceId,
                    "protocol": "bacnet",
                    "description": row.objectName or row.deviceId,
                    "host": "NOT ASSIGNED",
                    "port": 47808,
                })

        for row in parsed.rows:
            if not self._is_point(row):
                continue

            device = self.twin_service.get_model().get_device(row.deviceId)
            if not device:
                warning = f"EDE WARNING: Device {row.deviceId} not defined for point {row.objectName}"
                self.warnings.append(warning)
                continue

            resolved = self.structure_resolver.resolve(row)
            self.structure_stats[resolved["source"]] += 1

            metric = resolved["metric"]
            building_id = resolved["hierarchy"]["buildingId"]
            floor_id = resolved["hierarchy"]["floorId"]
            room_id = resolved["hierarchy"]["roomId"]
            equipment_id = resolved["hierarchy"]["equipmentId"]

            hierarchy = {
                "site": self.hierarchy_builder.build_node({"id": site_id}),
                "building": self.hierarchy_builder.build_node({"id": building_id}),
                "floor": self.hierarchy_builder.build_node({"id": floor_id}),
                "room": self.hierarchy_builder.build_node({"id": room_id}),
                "equipment": self.hierarchy_builder.build_node({"id": equipment_id}),
            }

            bacnet_type = self.bacnet_type_resolver.resolve(row.objectType)

            self.twin_service.create_point(
                {
                    "id": self._build_point_id(row),
                    "name": row.objectName or "unknown",
                    "deviceId": row.deviceId,
                    "equipmentId": equipment_id,
                    "metric": metric,
                    "objectType": row.objectType,
                    "objectInstance": row.objectInstance,
                    "type": self._map_point_type(bacnet_type),
                    "bacnetType": {
                        "name": bacnet_type["name"],
                        "category": bacnet_type["category"],
                    } if bacnet_type.get("name") else None,
                    "writable": self._is_writable(row.objectType),
                    "unit": row.unit,
                    "description": row.description,
                    "scale": 1,
                    "offset": 0,
                    "stateText": row.stateText or (
                        ["Inactive", "Active"]
                        if bacnet_type.get("class") == "binary"
                        else None
                    ),
                },
                hierarchy,
            )

    def get_structure_stats(self):
        return self.structure_stats

    def _is_device(self, row: EdeRow) -> bool:
        return row.objectType == "8"

    def _is_point(self, row: EdeRow) -> bool:
        try:
            type_number = int(row.objectType)
        except (TypeError, ValueError):
            return False

        if type_number == 8:
            return False

        excluded_types = [25, 52]
        return type_number not in excluded_types

    def _build_point_id(self, row: EdeRow) -> str:
        return f"{row.deviceId}:{row.objectType}:{row.objectInstance}"

    def _map_point_type(self, object_type: dict) -> str:
        if object_type.get("class") == "binary":
            return "digital"
        if object_type.get("class") == "multistate":
            return "analog"
        return "analog"

    def _is_writable(self, object_type: str) -> bool:
        return "O" in object_type