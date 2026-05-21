from src.services.protocols.bacnet.bacnet_type_resolver import BacnetTypeResolver


class BacnetIngestionStrategy:
    def __init__(self):
        self.bacnet_type_resolver = BacnetTypeResolver()

    def import_device(self, device: dict, context: dict, twin_service) -> None:
        for p in device.get("puntos", []):
            add = p.get("add", "")
            parts_add = add.split("-")
            object_type = str(parts_add[0]) if len(parts_add) > 0 else "unknown"
            object_instance = str(parts_add[1]) if len(parts_add) > 1 else "unknown"

            bacnet_type = self.bacnet_type_resolver.resolve(object_type)

            parts = (p.get("shortName") or "").split("'")
            equipment_id = parts[-2] if len(parts) >= 2 else "NOT_ASSIGNED"
            metric = parts[-1] if len(parts) >= 1 and parts[-1] else "unknown"

            hierarchy = context["buildHierarchy"](p.get("area"), equipment_id)

            twin_service.create_point(
                {
                    "id": f'{device["device_id"]}:{object_type}:{object_instance}',
                    "name": p.get("shortName") or "",
                    "description": p.get("desc") or "",
                    "deviceId": str(device["device_id"]),
                    "equipmentId": equipment_id,
                    "metric": metric,
                    "objectType": object_type,
                    "objectInstance": object_instance,
                    "bacnetType": bacnet_type,
                    "type": "digital" if p.get("digital") else "analog",
                    "writable": bool(p.get("write")),
                    "unit": p.get("unidad") or "",
                    "scale": p.get("escala") if p.get("escala") is not None else 1,
                    "offset": p.get("desplazamiento") if p.get("desplazamiento") is not None else 0,
                    "source": "physical",
                    "stateText": ["Inactive", "Active"] if p.get("digital") else None,
                },
                hierarchy,
            )