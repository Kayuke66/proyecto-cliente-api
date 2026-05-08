# Proyecto Cliente API

Cliente en Python para consumir una API REST local documentada con Swagger UI / OpenAPI.

## Descripción

Este proyecto forma parte de unas prácticas de empresa y tiene como objetivo desarrollar un cliente en Python capaz de consumir una API REST local, con una estructura profesional, control de versiones, documentación y tests.

La API utilizada corresponde al servicio **Santra Edge Agent Backend Service**, que expone su documentación en Swagger UI.

## Objetivos del proyecto

- Consumir endpoints de la API REST desde Python.
- Entender y utilizar Swagger UI / OpenAPI como referencia técnica del contrato de la API.
- Mantener una estructura de proyecto profesional.
- Gestionar versiones con Git y GitHub.
- Documentar cambios con `CHANGELOG.md`.
- Añadir tests con `pytest`.

## Tecnologías utilizadas

- Python
- requests
- pytest
- Git / GitHub
- PyCharm
- Swagger UI / OpenAPI
- uv

## Estructura del proyecto

```text
proyecto-cliente-api/
├── src/
│   └── api_client/
│       ├── __init__.py
│       ├── client.py
│       ├── config.py
│       ├── digital_twin.py
│       ├── health.py
│       ├── main.py
│       └── system.py
├── tests/
├── docs/
├── .gitignore
├── CHANGELOG.md
├── README.md
├── pyproject.toml
└── uv.lock
```

## Requisitos

- Python instalado.
- Entorno virtual configurado.
- API local arrancada en `http://localhost:3000`.
- Acceso a Swagger UI en `http://localhost:3000/api/docs`.

## Instalación

1. Clonar el repositorio.
2. Acceder a la carpeta del proyecto.
3. Activar el entorno virtual.
4. Instalar dependencias.

Con `pip`:

```bash
pip install requests pytest
```

Si usas `uv`:

```bash
uv sync
```

## Ejecución

Actualmente el punto de entrada del proyecto es `main.py`, que se usa como lanzador manual para probar endpoints durante el desarrollo.

En PyCharm, lo normal es ejecutar `main.py` como archivo principal del proyecto.

## Endpoints GET implementados

### Health
- `GET /api/health`

### System
- `GET /api/version`

### Digital Twin
- `GET /api/digital-twin/tree`
- `GET /api/digital-twin/devices`
- `GET /api/digital-twin/devices/{id}` — requiere `device_id`
- `GET /api/digital-twin/devices/{id}/points` — requiere `device_id`
- `GET /api/digital-twin/equipments/{id}/points` — requiere `equipment_id`
- `GET /api/digital-twin/points`

## Endpoints POST previstos / en implementación

### Requieren `requestBody`
- `POST /api/digital-twin/import/ede`
- `POST /api/digital-twin/import/santra-legacy-json`

### No requieren `requestBody`
- `POST /api/digital-twin/save`
- `POST /api/digital-twin/load`

## Validaciones actuales

Los endpoints GET que incluyen `{id}` requieren un identificador obligatorio. El cliente valida estos parámetros antes de construir la URL para evitar llamadas inválidas.

## Tests

El proyecto utiliza `pytest` para pruebas automatizadas.

Actualmente se están incorporando:
- tests del cliente base HTTP;
- tests de validación de parámetros obligatorios;
- tests para métodos `GET` y `POST`.

## Estado actual

El proyecto ya cuenta con:
- una estructura profesional de carpetas;
- un cliente base reutilizable;
- varios endpoints `GET` implementados;
- versionado inicial del proyecto;
- integración con Git y GitHub;
- documentación inicial;
- preparación de validaciones y tests;
- inicio del soporte para peticiones `POST`.

## Próximos pasos

- Completar la implementación real de endpoints `POST` a partir de Swagger UI.
- Ampliar los tests con más casos de error y validación.
- Mejorar la reutilización del cliente HTTP.
- Documentar ejemplos de uso de cada endpoint.
- Valorar una interfaz visual si sobra tiempo.

## Versionado

Este proyecto sigue Semantic Versioning (`SemVer`) y documenta sus cambios en `CHANGELOG.md`.
