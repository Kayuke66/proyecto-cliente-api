from src.api_client.client import APIClient

def digital_twin_tree():
    client = APIClient()
    return client.get("/api/digital-twin/tree")

def get_devices():
    client = APIClient()
    return client.get("/api/digital-twin/devices")

def get_device_by_id(device_id):
    if not device_id:
        raise ValueError("El ID es obligatorio")
    client = APIClient()
    return client.get(f"/api/digital-twin/devices/{device_id}")

def get_device_points(device_id):
    if not device_id:
        raise ValueError("El ID es obligatorio")
    client = APIClient()
    return client.get(f"/api/digital-twin/devices/{device_id}/points")

def get_equipment_points(equipment_id):
    if not equipment_id:
        raise ValueError("El ID es obligatorio")
    client = APIClient()
    return client.get(f"/api/digital-twin/equipments/{equipment_id}/points")

def get_all_points():
    client = APIClient()
    return client.get("/api/digital-twin/points")

def import_ede(ede_content):
    if not ede_content:
        raise ValueError("La petición requiere el archivo EDE.")

    client = APIClient()
    return client.post("/api/digital-twin/import/ede",
                       ede_content,
                       content_type="text/plain"
    )

def import_ede_from_file(filename: str, content: bytes) -> dict:
    endpoint = "/digital-twin/import/ede"

    files = {
        "file": (filename, content, "text/plain"),  # o el content-type que corresponda
    }

    response = APIClient.post(endpoint, files=files)
    return response

def import_santra_legacy_json(data: dict) -> dict:
    endpoint = "/digital-twin/import/santra-legacy-json"

    response = APIClient.post(endpoint, json=data)
    return response

def save_digital_twin():
    client = APIClient()
    return client.post("/api/digital-twin/save")

def load_digital_twin():
    client = APIClient()
    return client.post("/api/digital-twin/load")