import requests

from api_client.config import DEF_URL, DEF_TIMEOUT

def digital_twin_tree():
    endpoint = "/api/digital-twin/tree"
    url = DEF_URL + endpoint

    try:
        respuesta = requests.get(url, timeout=5)
        respuesta.raise_for_status()

        datos = respuesta.json()
        return datos

    except requests.exceptions.ConnectionError:
        print("La conexión con la API no ha sido posible.")
    except requests.exceptions.Timeout:
        print("Se agotó el tiempo de espera de la API.")
    except requests.exceptions.HTTPError as error:
        print("Error:", error)
    except ValueError:
        print("No hay contenido JSON válido.")
    except requests.exceptions.RequestException as error:
        print("Error en su petición: ", error)

    return None

