from api_client.client import APIClient


class MockPostResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return {"resultado": "ok"}


def test_post_con_body_devuelve_json(monkeypatch):
    def mock_post(self, url, json, timeout):
        return MockPostResponse()

    monkeypatch.setattr("requests.sessions.Session.post", mock_post)

    client = APIClient()
    result = client.post("/api/digital-twin/import/santra-legacy-json", {"idPlanta": "TESTSITE"})

    assert result == {"resultado": "ok"}