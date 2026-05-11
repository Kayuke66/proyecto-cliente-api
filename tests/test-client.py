import requests

from api_client.client import APIClient


class MockEmptyResponse:
    text = ""

    def raise_for_status(self):
        pass

    def json(self):
        return None

class MockHttpJsonErrorResponse:
    text = '{"error": {"code": "ERR_SMA_007"}}'

    def raise_for_status(self):
        raise requests.exceptions.HTTPError("400 Client Error")

    def json(self):
        return {
            "error": {
                "code": "ERR_SMA_007",
                "message": "EDE file validation failed",
                "details": [
                    "EDE does not contain any device definition"
                ]
            }
        }


def test_post_devuelve_none_si_hay_http_error_con_json(monkeypatch):
    def mock_post(self, url, data, headers, timeout):
        return MockHttpJsonErrorResponse()

    monkeypatch.setattr("requests.sessions.Session.post", mock_post)

    client = APIClient()
    result = client.post(
        "/api/digital-twin/import/ede",
        "contenido de prueba",
        content_type="text/plain"
    )

    assert result is None

def test_get_da_none_si_la_respuesta_esta_vacia(monkeypatch):
    def mock_get(self, url, timeout):
        return MockEmptyResponse()

    monkeypatch.setattr("requests.sessions.Session.get", mock_get)

    client = APIClient()
    result = client.get("/api/digital-twin/tree")

    assert result is None


class MockErrorResponse:
    text = "not found"

    def raise_for_status(self):
        raise requests.exceptions.HTTPError("404 Client Error")

    def json(self):
        return {"error": "not found"}


def test_post_da_none_si_hay_http_error(monkeypatch):
    def mock_post(self, url, timeout):
        return MockErrorResponse()

    monkeypatch.setattr("requests.sessions.Session.post", mock_post)

    client = APIClient()
    result = client.post("/api/digital-twin/load")

    assert result is None


class MockResponse:
    text = '{"status": "ok"}'

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


class MockTextResponse:
    text = "Respuesta en texto plano"

    def raise_for_status(self):
        pass

    def json(self):
        raise ValueError("No es JSON")


def test_get_devuelve_texto_si_no_es_json(monkeypatch):
    def mock_get(self, url, timeout):
        return MockTextResponse()

    monkeypatch.setattr("requests.sessions.Session.get", mock_get)

    client = APIClient()
    result = client.get("/api/texto")

    assert result == "Respuesta en texto plano"


class MockPostResponse:
    text = '{"resultado": "ok"}'

    def raise_for_status(self):
        pass

    def json(self):
        return {"resultado": "ok"}


def test_post_devuelve_json_correctamente(monkeypatch):
    def mock_post(self, url, json, timeout):
        return MockPostResponse()

    monkeypatch.setattr("requests.sessions.Session.post", mock_post)

    client = APIClient()
    result = client.post("/api/digital-twin/save", {"name": "prueba"})

    assert result == {"resultado": "ok"}

class MockTextPostResponse:
    text = '{"devices": 0, "points": 0}'

    def raise_for_status(self):
        pass

    def json(self):
        return {"devices": 0, "points": 0}


def test_post_texto_plano_devuelve_json(monkeypatch):
    def mock_post(self, url, data, headers, timeout):
        assert headers["Content-Type"] == "text/plain"
        return MockTextPostResponse()

    monkeypatch.setattr("requests.sessions.Session.post", mock_post)

    client = APIClient()
    result = client.post(
        "/api/digital-twin/import/ede",
        "B_01'STecnica'Box1...",
        content_type="text/plain"
    )

    assert result == {"devices": 0, "points": 0}