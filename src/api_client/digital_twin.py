from api_client.client import APIClient

def digital_twin_tree():
    client = APIClient()
    return client.get("/api/digital-twin/tree")

def get_devices():
    client = APIClient()
    return client.get("/api/digital-twin/devices")

def get_device_by_id(device_id):
    client = APIClient()
    return client.get(f"/api/digital-twin/devices/{device_id}")

def get_device_points(device_id):
    client = APIClient()
    return client.get(f"/api/digital-twin/devices/{device_id}/points")

def get_equipment_points(equipment_id):
    client = APIClient()
    return client.get(f"/api/digital-twin/equipments/{equipment_id}/points")

def get_all_points():
    client = APIClient()
    return client.get("/api/digital-twin/points")