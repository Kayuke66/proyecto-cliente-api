from src.core.errors.catalog import ERRORS
from src.core.errors.model import SantraError
from src.services.ingestion.hierarchy_builder import HierarchyBuilder
from src.services.protocols.bacnet.bacnet_ingestion_strategy import BacnetIngestionStrategy
from src.services.protocols.modbus.modbus_ingestion_strategy import ModbusIngestionStrategy


class SantraLegacyJsonInterpreter:
    def __init__(self, twin_service):
        self.twin_service = twin_service
        self.hierarchy_builder = HierarchyBuilder()

    def import_data(self, data: dict) -> None:
        site_id = data["idPlanta"]
        building_id = data["idPlanta"]

        site_name = data["denominacion"]
        building_name = data["denominacion"]

        self.twin_service.create_device({
            "id": "virtual",
            "name": "Virtual Device",
            "description": "Virtual computed points",
            "protocol": "virtual",
            "host": "NOT ASSIGNED",
            "port": 0,
            "unitId": 0,
        })

        site_metadata = {
            "company": data.get("legalEntity") or "NOT ASSIGNED",
            "language": data.get("language") or "es",
        }

        building_metadata = {
            "location": data.get("localizacion"),
            "lat": data.get("latitud"),
            "lon": data.get("longitud"),
            "surface": data.get("superficie_m2"),
            "volume": data.get("volumen_m3"),
            "capacity": data.get("aforo"),
        }

        areas_map = {
            a["descripcion"]: a
            for a in (data.get("areas") or [])
            if a.get("descripcion")
        }

        for device in data.get("dispositivos", []):
            self.twin_service.create_device({
                "id": str(device["device_id"]),
                "name": device["device_name"],
                "description": device["device_name"],
                "protocol": device["protocolo"],
                "host": device.get("host") or "NOT ASSIGNED",
                "port": 47808 if device.get("protocolo") == "bacnet" else (device.get("port") or 0),
                "unitId": device.get("dir_fisica") or 0,
            })

            context = {
                "siteId": site_id,
                "buildingId": building_id,
                "siteName": site_name,
                "buildingName": building_name,
                "siteMetadata": site_metadata,
                "buildingMetadata": building_metadata,
                "areasMap": areas_map,
                "buildHierarchy": lambda area, equipment_id, site_id=site_id, building_id=building_id,
                site_name=site_name, building_name=building_name, site_metadata=site_metadata,
                building_metadata=building_metadata, areas_map=areas_map:
                    self._build_area_hierarchy(
                        area,
                        equipment_id,
                        site_id,
                        building_id,
                        site_name,
                        building_name,
                        site_metadata,
                        building_metadata,
                        areas_map,
                    ),
                "normalizeMetric": self._normalize_metric,
            }

            strategy = self._get_strategy(device.get("protocolo"))
            strategy.import_device(device, context, self.twin_service)

        virtual_points = [
            *[
                {
                    "add": d["add"],
                    "desc": d["punto"]["desc"],
                    "area": d["punto"].get("area"),
                    "unidad": d["punto"].get("unidad"),
                    "escala": 1,
                    "datos": [{
                        "device_id": d["punto"].get("device_id"),
                        "add": d["punto"].get("add"),
                        "operacion": "delta",
                    }],
                }
                for d in (data.get("deltas") or [])
            ],
            *[
                {
                    "add": c["add"],
                    "desc": c["desc"],
                    "area": c.get("area"),
                    "unidad": c.get("unidad"),
                    "escala": c.get("escala"),
                    "datos": c.get("datos", []),
                }
                for c in (data.get("calculados") or [])
            ],
        ]

        for v in virtual_points:
            dependencies = [
                dep for dep in
                [self._build_dependency_id(d) for d in v.get("datos", []) if d.get("add")]
                if dep
            ]

            hierarchy = self._build_hierarchy(
                site_id=site_id,
                building_id=building_id,
                floor_id=v.get("area") or "default",
                room_id="default",
                equipment_id="NOT_ASSIGNED",
                site_name=site_name,
                building_name=building_name,
                floor_name=v.get("area") or "default",
                site_metadata=site_metadata,
                building_metadata=building_metadata,
                floor_metadata={},
            )

            self.twin_service.create_point(
                {
                    "id": f'virtual:{v["add"]}',
                    "name": v["desc"],
                    "description": v["desc"],
                    "deviceId": "virtual",
                    "equipmentId": "VIRTUAL",
                    "metric": self._normalize_metric(v["desc"]),
                    "objectType": "virtual",
                    "objectInstance": str(v["add"]),
                    "type": "analog",
                    "writable": False,
                    "unit": v.get("unidad") or "",
                    "scale": v.get("escala") if v.get("escala") is not None else 1,
                    "offset": 0,
                    "source": "virtual",
                    "dependencies": dependencies,
                    "expression": v.get("datos", []),
                },
                hierarchy,
            )

    def _get_strategy(self, protocol: str):
        protocol_name = (protocol or "").lower()

        if protocol_name == "bacnet":
            return BacnetIngestionStrategy()

        if protocol_name == "modbus":
            return ModbusIngestionStrategy()

        err = ERRORS["UNSUPPORTED_PROTOCOL"]
        raise SantraError(
            code=err["code"],
            message=err["message"],
            category=err["category"],
            module="SantraLegacyJsonInterpreter.getStrategy",
            meta={"protocol": protocol},
            status_code=400,
        )

    def _normalize_metric(self, text: str) -> str:
        return (text or "unknown").lower().replace(" ", "_")

    def _build_dependency_id(self, d: dict) -> str:
        add = d.get("add")
        if not add:
            return ""

        if add.startswith("d") or add.startswith("c"):
            return f"virtual:{add}"

        if d.get("device_id") is not None:
            return f'{d["device_id"]}:{add}'

        return add

    def _build_area_hierarchy(self, area, equipment_id, site_id, building_id, site_name, building_name, site_metadata, building_metadata, areas_map):
        area_value = area or "default"
        area_data = areas_map.get(area_value, {})

        floor_metadata = {
            "surface": area_data.get("superficie_m2"),
            "volume": area_data.get("volumen_m3"),
            "capacity": area_data.get("aforo"),
        }

        return self._build_hierarchy(
            site_id=site_id,
            building_id=building_id,
            floor_id=area_value,
            room_id="default",
            equipment_id=equipment_id,
            site_name=site_name,
            building_name=building_name,
            floor_name=area_value,
            site_metadata=site_metadata,
            building_metadata=building_metadata,
            floor_metadata=floor_metadata,
        )

    def _build_hierarchy(self, site_id, building_id, floor_id, room_id, equipment_id,
                         site_name=None, building_name=None, floor_name=None,
                         site_metadata=None, building_metadata=None, floor_metadata=None):
        return {
            "site": self.hierarchy_builder.build_node({
                "id": site_id,
                "name": site_name or site_id,
                "description": site_name or site_id,
                "metadata": site_metadata,
            }),
            "building": self.hierarchy_builder.build_node({
                "id": building_id,
                "name": building_name or building_id,
                "description": building_name or building_id,
                "metadata": building_metadata,
            }),
            "floor": self.hierarchy_builder.build_node({
                "id": floor_id,
                "name": floor_name or floor_id,
                "description": floor_name or floor_id,
                "metadata": floor_metadata,
            }),
            "room": self.hierarchy_builder.build_node({
                "id": room_id,
                "name": room_id,
                "description": room_id,
            }),
            "equipment": self.hierarchy_builder.build_node({
                "id": equipment_id,
                "name": equipment_id,
                "description": equipment_id,
            }),
        }