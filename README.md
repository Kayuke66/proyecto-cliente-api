# Proyecto Cliente API

Cliente en Python para consumir una API REST local documentada con Swagger UI / OpenAPI.

## Descripción

Este proyecto forma parte de unas prácticas de empresa y tiene como objetivo desarrollar un cliente en Python capaz de consumir una API REST local, con una estructura profesional, control de versiones, documentación y tests.

La API utilizada corresponde al servicio **Santra Edge Agent Backend Service**, que expone su documentación en Swagger UI.

## Objetivos del proyecto

- Consumir endpoints de la API REST desde Python.
- Entender y utilizar Swagger UI / OpenAPI como base para implementar el cliente.
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

- Python instalado
- Entorno virtual configurado
- API local arrancada en `http://localhost:3000`
- Acceso a la documentación Swagger en `http://localhost:3000/api/docs`

## Instalación

1. Clonar el repositorio.
2. Acceder a la carpeta del proyecto.
3. Activar el entorno virtual.
4. Instalar dependencias.

Ejemplo:

```bash
pip install requests pytest
```

Si usas `uv`:

```bash
uv sync
```

## Ejecución

Para ejecutar el proyecto desde PyCharm, usa `main.py` como punto de entrada.

También puedes ejecutarlo desde terminal según la configuración del entorno y de imports del proyecto.

## Endpoints implementados actualmente

### Health
- `GET /api/health`

### System
- `GET /api/version`

### Digital Twin
- `GET /api/digital-twin/tree`
- `GET /api/digital-twin/devices`
- `GET /api/digital-twin/devices/{id}`
- `GET /api/digital-twin/devices/{id}/points`
- `GET /api/digital-twin/equipments/{id}/points`
- `GET /api/digital-twin/points`

## Estado actual

El proyecto ya cuenta con:
- una estructura profesional de carpetas;
- un cliente base reutilizable;
- varios endpoints `GET` implementados;
- integración con Git y GitHub;
- documentación inicial;
- preparación para tests.

## Próximos pasos

- Añadir tests con `pytest`.
- Ampliar el cliente con endpoints `POST`.
- Mejorar la reutilización del cliente HTTP.
- Documentar mejor el uso de Swagger UI dentro del proyecto.
- Valorar una interfaz si sobra tiempo.

## Versionado

Este proyecto sigue Semantic Versioning (`SemVer`) y documenta sus cambios en `CHANGELOG.md`.