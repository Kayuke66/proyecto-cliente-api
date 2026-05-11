from src.api_client.client import APIClient

def get_version():
    client = APIClient()
    return client.get("/api/version")