import requests

from api_client.client import APIClient


def test_get_devuelve_none_si_hay_error_de_conexion(monkeypatch):
    def mock_get(self, url, timeout):
        raise requests.exceptions.ConnectionError()

    monkeypatch.setattr("requests.sessions.Session.get", mock_get)

    client = APIClient()
    result = client.get("/api/health")

    assert result is None