from api_client.client import APIClient

def get_health():
    client = APIClient()
    return client.get("/api/health")