from src.schemas.digital_twin import CompactPointDto, DeviceDto, PointDto
from src.services.digital_twin_models import Device, Point
from src.services.ingestion.ede.ede_parser import EdeParser
from src.services.ingestion.ede.ede_validation import EdeValidator
from src.services.ingestion.ede.ede_interpreter import EdeInterpreter
from src.core.errors.model import SantraError
from src.core.errors.catalog import ERRORS
from src.services.ingestion.santra_legacy.santra_legacy_json_parser import SantraLegacyJsonParser
from src.services.ingestion.santra_legacy.santra_legacy_json_interpreter import SantraLegacyJsonInterpreter

class DigitalTwinService:
    def __init__(self, digital_twin, persistence):
        self.digital_twin = digital_twin
        self.persistence = persistence

    def init(self):
        loaded = self.persistence.load_digital_twin()

        if loaded.get_all_points():
            self.digital_twin = loaded

    def save(self):
        self.persistence.save_digital_twin(self.digital_twin)

    def load(self):
        self.digital_twin = self.persistence.load_digital_twin()


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
                    description=getattr(point, "description", "") or "",
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
                    host=getattr(device, "host", None),
                    port=getattr(device, "port", None),
                    unitId=getattr(device, "unitId", 0) or 0,
                ).model_dump()
            )

        return result

    def get_device(self, device_id: str):
        device = self.digital_twin.get_device(device_id)

        if not device:
            return None

        return DeviceDto(
            id=device.id,
            name=device.name,
            description=getattr(device, "description", None),
            protocol=getattr(device, "protocol", None),
            host=getattr(device, "host", None),
            port=getattr(device, "port", None),
            unitId=getattr(device, "unitId", 0) or 0,
        ).model_dump()

    def get_points_by_device(self, device_id: str):
        result = []

        for point in self.digital_twin.get_points_by_device(device_id):
            result.append(
                PointDto(
                    id=point.id,
                    name=point.name,
                    description=getattr(point, "description", "") or "",
                    deviceId=point.deviceId,
                    metric=point.metric,
                    objectType=point.objectType,
                    objectInstance=point.objectInstance,
                    bacnetType=getattr(point, "bacnetType"),
                    type=point.type,
                    writable=point.writable,
                    unit=getattr(point, "unit", "") or "",
                    stateText=getattr(point, "stateText"),
                    scale=getattr(point, "scale"),
                    offset=getattr(point, "offset"),
                    source=getattr(point, "source"),
                    expression=getattr(point, "expression"),
                    dependencies=getattr(point, "dependencies"),
                    metadata=getattr(point, "metadata", None),
                ).model_dump()
            )

        return result

    def get_points_by_equipment(self, equipment_id: str):
        result = []

        for point in self.digital_twin.get_points_by_equipment(equipment_id):
            result.append(
                PointDto(
                    id=point.id,
                    name=point.name,
                    description=getattr(point, "description", "") or "",
                    deviceId=point.deviceId,
                    metric=point.metric,
                    objectType=point.objectType,
                    objectInstance=point.objectInstance,
                    bacnetType=getattr(point, "bacnetType"),
                    type=point.type,
                    writable=point.writable,
                    unit=getattr(point, "unit", "") or "",
                    stateText=getattr(point, "stateText"),
                    scale=getattr(point, "scale"),
                    offset=getattr(point, "offset"),
                    source=getattr(point, "source"),
                    expression=getattr(point, "expression"),
                    dependencies=getattr(point, "dependencies"),
                    metadata=getattr(point, "metadata", None),
                ).model_dump()
            )

        return result

    def get_points(self):
        result = []

        for point in self.digital_twin.get_all_points():
            result.append(
                PointDto(
                    id=point.id,
                    name=point.name,
                    description=getattr(point, "description", "") or "",
                    deviceId=point.deviceId,
                    metric=point.metric,
                    objectType=point.objectType,
                    objectInstance=point.objectInstance,
                    bacnetType=getattr(point, "bacnetType"),
                    type=point.type,
                    writable=point.writable,
                    unit=getattr(point, "unit", "") or "",
                    stateText=getattr(point, "stateText"),
                    scale=getattr(point, "scale"),
                    offset=getattr(point, "offset"),
                    source=getattr(point, "source"),
                    expression=getattr(point, "expression"),
                    dependencies=getattr(point, "dependencies"),
                    metadata=getattr(point, "metadata", None),
                ).model_dump()
            )

        return result


    def get_model(self):
        return self.digital_twin

    def create_device(self, props: dict):
        device = Device(
            id=props["id"],
            name=props["name"],
            description=props.get("description"),
            protocol=props.get("protocol"),
            vendor=props.get("vendor"),
            model=props.get("model"),
            host=props.get("host"),
            port=props.get("port"),
            unitId=props.get("unitId"),
            metadata=props.get("metadata"),
        )

        self.digital_twin.add_device(device)
        return device

    def create_point(self, props: dict, hierarchy: dict | None = None):
        device = self.digital_twin.get_device(props["deviceId"])

        if not device:
            raise Exception(f'Device {props["deviceId"]} not found')

        point = Point(
            id=props["id"],
            name=props["name"],
            description=props.get("description"),
            deviceId=props["deviceId"],
            metric=props["metric"],
            objectType=props["objectType"],
            objectInstance=props["objectInstance"],
            bacnetType=props.get("bacnetType"),
            type=props["type"],
            writable=props["writable"],
            unit=props.get("unit"),
            stateText=props.get("stateText"),
            scale=props.get("scale"),
            offset=props.get("offset"),
            source=props.get("source"),
            expression=props.get("expression"),
            dependencies=props.get("dependencies"),
            metadata=props.get("metadata"),
            equipmentId=props.get("equipmentId"),
        )

        self.digital_twin.add_point(point, hierarchy)
        return point

    def import_ede(self, content: str):
        self.digital_twin.clear()

        parser = EdeParser()
        parsed = parser.parse(content)

        validator = EdeValidator()
        validation = validator.validate(parsed)

        if not validation["isValid"]:
            return {
                "siteId": parsed.metadata.projectName or "default",
                "devices": 0,
                "points": 0,
                "errors": validation["errors"],
            }

        interpreter = EdeInterpreter(self)
        interpreter.import_data(parsed)
        structure_stats = interpreter.get_structure_stats()

        self.save()

        return {
            "siteId": parsed.metadata.projectName or "default",
            "devices": len(self.digital_twin.get_all_devices()),
            "points": len(self.digital_twin.get_all_points()),
            "structureStats": structure_stats,
        }

    def import_santra_legacy_json(self, content: str):
        self.digital_twin.clear()

        try:
            parser = SantraLegacyJsonParser()
            data = parser.parse(content)

            interpreter = SantraLegacyJsonInterpreter(self)
            interpreter.import_data(data)

            self.save()

            return {
                "siteId": data["idPlanta"],
                "devices": len(self.get_devices()),
                "points": len(self.get_points()),
            }

        except SantraError:
            raise
        except Exception as error:
            err = ERRORS["IMPORT_SANTRA_LEGACY_FAILED"]
            raise SantraError(
                code=err["code"],
                message=err["message"],
                category=err["category"],
                module="DigitalTwinService.importSantraLegacyJson",
                meta={"details": str(error)},
                status_code=500,
            )

