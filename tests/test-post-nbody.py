from api_client.client import APIClient

class MockPostResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {"resultado": "ok"}

def test_post_sin_body_devuelve_json(monkeypatch):
    def mock_post(self, url, timeout):
        return MockPostResponse()

    monkeypatch.setattr("requests.sessions.Session.post", mock_post)

    client = APIClient()
    result = client.post("/api/digital-twin/save")

    assert result == {"resultado": "ok"}