import requests
from api_client.config import DEF_URL, DEF_TIMEOUT

class APIClient:
    def __init__(self, def_url=DEF_URL, timeout=DEF_TIMEOUT):
        self.def_url = def_url
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, endpoint):
        url = self.def_url + endpoint

        try:
            respuesta = self.session.get(url, timeout=self.timeout)
            respuesta.raise_for_status()
            return respuesta.json()

        except requests.exceptions.ConnectionError:
            print("La conexión con la API no se ha podido completar.")
        except requests.exceptions.Timeout:
            print("Su petición ha superado el tiempo de espera.")
        except requests.exceptions.HTTPError as error:
            print("Error de conexión HTTP:", error)
        except ValueError:
            print("La respuesta no contiene un JSON válido.")
        except requests.exceptions.RequestException as error:
            print("Error en la petición:", error)

        return None