import requests
from src.api_client.config import DEF_URL, DEF_TIMEOUT

class APIClient:
    def __init__(self, def_url=DEF_URL, timeout=DEF_TIMEOUT):
        self.def_url = def_url
        self.timeout = timeout
        self.session = requests.Session()

    def _process_response(self, respuesta):
        respuesta.raise_for_status()

        if not respuesta.text.strip():
            return None

        try:
            return respuesta.json()
        except ValueError:
            return respuesta.text

    def get(self, endpoint):
        url = self.def_url + endpoint

        try:
            respuesta = self.session.get(url, timeout=self.timeout)
            return self._process_response(respuesta)

        except requests.exceptions.ConnectionError:
            print("La conexión con la API no se ha podido completar.")
        except requests.exceptions.Timeout:
            print("Su petición ha superado el tiempo de espera.")
        except requests.exceptions.HTTPError as error:
            print("Error de conexión HTTP:", error)

            try:
                error_body = respuesta.json()
                print("Detalle del error: ", error_body)
            except Exception:
                pass

        except requests.exceptions.RequestException as error:
            print("Error en la petición:", error)

        return None

    def post(self, endpoint, data=None, content_type="application/json"):
        url = self.def_url + endpoint

        try:
            if data is None:
                respuesta = self.session.post(url, timeout=self.timeout)

            elif content_type == "text/plain":
                headers = {"Content-Type": "text/plain"}
                respuesta = self.session.post(url, data=data, headers=headers, timeout=self.timeout)

            else:
                respuesta = self.session.post(url, json=data, timeout=self.timeout)

            return self._process_response(respuesta)

        except requests.exceptions.ConnectionError:
            print("No se ha podido establecer conexión con la API.")
        except requests.exceptions.Timeout:
            print("La petición ha superado el tiempo de espera.")
        except requests.exceptions.HTTPError as error:
            print("Error HTTP:", error)

            try:
                error_body = respuesta.json()
                print("Detalle del error:", error_body)
            except Exception:
                pass

        except requests.exceptions.RequestException as error:
            print("Error en la petición:", error)

        return None