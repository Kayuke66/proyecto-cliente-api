from src.schemas.digital_twin import CompactPointDto, DeviceDto


class DigitalTwinService:
    def __init__(self, digital_twin):
        self.digital_twin = digital_twin

    def get_tree(self):
        tree: dict[str, dict] = {}

        for point in self.digital_twin.get_all_points():
            nodes = self.digital_twin.get_hierarchy(point.id)
            if not nodes:
                continue

            site = nodes["site"]
            building = nodes["building"]
            floor = nodes["floor"]
            room = nodes["room"]
            equipment = nodes["equipment"]

            tree.setdefault(
                site["id"],
                {
                    **site,
                    "buildings": {},
                },
            )
            s = tree[site["id"]]

            s["buildings"].setdefault(
                building["id"],
                {
                    **building,
                    "floors": {},
                },
            )
            b = s["buildings"][building["id"]]

            b["floors"].setdefault(
                floor["id"],
                {
                    **floor,
                    "rooms": {},
                },
            )
            f = b["floors"][floor["id"]]

            f["rooms"].setdefault(
                room["id"],
                {
                    **room,
                    "equipments": {},
                },
            )
            r = f["rooms"][room["id"]]

            r["equipments"].setdefault(
                equipment["id"],
                {
                    **equipment,
                    "points": [],
                },
            )
            e = r["equipments"][equipment["id"]]

            e["points"].append(
                CompactPointDto(
                    id=point.id,
                    name=point.name,
                    description=point.description,
                    deviceId=point.deviceId,
                    type=point.type,
                ).model_dump()
            )

        return tree

    def get_devices(self):
        result = []

        for device in self.digital_twin.get_all_devices():
            result.append(
                DeviceDto(
                    id=device.id,
                    name=device.name,
                    description=getattr(device, "description", None),
                    protocol=getattr(device, "protocol", None),
                    vendor=getattr(device, "vendor", None),
                    model=getattr(device, "model", None),
                ).model_dump()
            )

        return result