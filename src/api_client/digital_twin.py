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

def import_ede_from_file(file_path):
    if not file_path:
        raise ValueError("Se requiere la ruta del archivo EDE")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            ede_content = file.read()
    except FileNotFoundError:
        raise ValueError(f"No se encontró el archivo: {file_path}")

    if not ede_content.strip():
        raise ValueError("El archivo EDE está vacío")

    return import_ede(ede_content)

def import_santra_legacy_json(data):
    if not data:
        raise ValueError("Se requiere el archivo .json")

    required_fields = ["idPlanta", "denominacion", "legalEntity", "language", "dispositivos"]

    for field in required_fields:
        if field not in data:
            raise ValueError(f"No se ha introducido el siguiente campo: {field}")

    client = APIClient()
    return client.post("/api/digital-twin/import/santra-legacy-json", data)

def save_digital_twin():
    client = APIClient()
    return client.post("/api/digital-twin/save")

def load_digital_twin():
    client = APIClient()
    return client.post("/api/digital-twin/load")