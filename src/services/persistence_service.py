import json
from pathlib import Path

from src.services.digital_twin_store import InMemoryDigitalTwin
from src.services.digital_twin_models import Device, Point


class PersistenceService:
    def __init__(self, file_path: str = "data/digital_twin.json"):
        self.file_path = Path(file_path)

    def init(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def save_digital_twin(self, digital_twin: InMemoryDigitalTwin):
        payload = {
            "devices": [device.__dict__ for device in digital_twin.get_all_devices()],
            "points": [point.__dict__ for point in digital_twin.get_all_points()],
            "hierarchy_by_point": digital_twin._hierarchy_by_point,
        }

        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def load_digital_twin(self) -> InMemoryDigitalTwin:
        twin = InMemoryDigitalTwin()

        if not self.file_path.exists():
            return twin

        with self.file_path.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        for raw_device in payload.get("devices", []):
            twin.add_device(Device(**raw_device))

        for raw_point in payload.get("points", []):
            twin.add_point(Point(**raw_point))

        twin._hierarchy_by_point = payload.get("hierarchy_by_point", {})
        return twin