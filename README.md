# Santra Python API

Reimplementación en Python/FastAPI de una API originalmente construida en Node.js, empezando por el endpoint `GET /api/health`.

## Objetivo

Este proyecto crea una versión autónoma en Python de la API, manteniendo la arquitectura funcional del proyecto original:

- rutas
- controlador
- servicios
- checks de health
- schemas de respuesta

La idea no es copiar literalmente el código Node, sino trasladar su diseño y comportamiento al ecosistema Python/FastAPI.

## Estado actual

Implementado o preparado:

- `GET /api/health`
- arquitectura por capas
- checks independientes de health
- respuesta agregada con `status`, `timestamp` y `checks`
- documentación Swagger automática con FastAPI

Pendiente:

- migrar el resto de endpoints
- unificar manejo de errores global
- completar documentación técnica endpoint por endpoint
- tests automáticos

## Estructura recomendada

```text
src/
  __init__.py
  app.py
  api/
    __init__.py
    routes/
      __init__.py
      health.py
  controllers/
    __init__.py
    health_controller.py
  services/
    __init__.py
    health_monitor/
      __init__.py
      health_monitor_service.py
      checks/
        __init__.py
        health_check_interface.py
        event_loop_check.py
        uptime_check.py
        memory_check.py
  schemas/
    __init__.py
    health.py
```

## Requisitos

- Python 3.11 o superior
- `fastapi`
- `uvicorn`
- `pydantic`
- `psutil`

## Instalación

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Desde la raíz del proyecto:

```bash
uvicorn src.app:app --reload
```

## Probar el endpoint health

### Swagger

Abrir:

- `http://127.0.0.1:8000/docs`

### Curl

```bash
curl -X GET "http://127.0.0.1:8000/api/health" -H "accept: application/json"
```

## Respuesta esperada aproximada

```json
{
  "status": "ok",
  "timestamp": 1716020000000,
  "checks": {
    "event_loop": {
      "status": "ok",
      "message": "",
      "timestamp": 1716020000000,
      "meta": {
        "delayMs": 1.2
      }
    },
    "uptime": {
      "status": "ok",
      "message": "",
      "timestamp": 1716020000000,
      "meta": {
        "uptimeSeconds": 5
      }
    },
    "memory": {
      "status": "ok",
      "message": "",
      "timestamp": 1716020000000,
      "meta": {
        "heapUsedMb": 25.1
      }
    }
  }
}
```

## Diferencias respecto al proyecto Node

- Se mantiene la misma arquitectura lógica, pero adaptada a FastAPI.
- `Router` pasa a `APIRouter`.
- Los DTO/interfaces de TypeScript pasan a modelos Pydantic.
- Algunos checks se adaptan al runtime Python; por ejemplo, el control del event loop no se mide exactamente igual que en Node.
- El objetivo es equivalencia funcional, no copia literal del runtime original.

## Motivo de separar este proyecto del antiguo

La carpeta antigua contenía imports y dependencias heredadas del cliente previo, como referencias a `src.api_client`, que provocaban errores de importación al arrancar la nueva API.

Separar el proyecto permite:

- eliminar dependencias antiguas
- tener una arquitectura limpia
- evitar conflictos de imports
- documentar claramente la transición de Node a Python

## Próximos pasos sugeridos

1. Confirmar que `GET /api/health` funciona correctamente.
2. Añadir tests básicos.
3. Migrar `/api/version`.
4. Migrar los endpoints de digital twin uno a uno.
5. Unificar convenciones de errores y documentación OpenAPI.
