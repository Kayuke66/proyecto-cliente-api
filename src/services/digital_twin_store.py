class InMemoryDigitalTwin:
    def __init__(self):
        self._devices = []
        self._points = []
        self._hierarchy_by_point = {}

    def get_all_devices(self):
        return self._devices

    def get_all_points(self):
        return self._points

    def get_hierarchy(self, point_id: str):
        return self._hierarchy_by_point.get(point_id)


digital_twin = InMemoryDigitalTwin()