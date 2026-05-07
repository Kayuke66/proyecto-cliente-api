from api_client.client import APIClient

class MockResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {"status": "ok"}


def test_get_devuelve_json_correctamente(monkeypatch):
    def mock_get(self, url, timeout):
        return MockResponse()

    monkeypatch.setattr("requests.sessions.Session.get", mock_get)

    client = APIClient()
    result = client.get("/api/health")

    assert result == {"status": "ok"}