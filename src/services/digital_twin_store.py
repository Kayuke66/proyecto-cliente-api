class InMemoryDigitalTwin:
    def __init__(self):
        self._devices = []
        self._points = []
        self._hierarchy_by_point = {}

    def clear(self):
        self._devices = []
        self._points = []
        self._hierarchy_by_point = {}

    def add_device(self, device):
        self._devices.append(device)

    def add_point(self, point, hierarchy=None):
        self._points.append(point)
        if hierarchy:
            self._hierarchy_by_point[point.id] = hierarchy

    def get_all_devices(self):
        return self._devices

    def get_device(self, device_id: str):
        for device in self._devices:
            if device.id == device_id:
                return device
        return None

    def get_all_points(self):
        return self._points

    def get_points_by_device(self, device_id: str):
        return [point for point in self._points if point.deviceId == device_id]

    def get_points_by_equipment(self, equipment_id: str):
        result = []

        for point in self._points:
            hierarchy = self._hierarchy_by_point.get(point.id)
            if not hierarchy:
                continue

            equipment = hierarchy.get("equipment")
            if equipment and equipment.get("id") == equipment_id:
                result.append(point)

        return result

    def get_hierarchy(self, point_id: str):
        return self._hierarchy_by_point.get(point_id)

digital_twin = InMemoryDigitalTwin()