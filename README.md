# Proyecto API Client
Cliente hecho en Python que consume una API REST local documentada con Swagger UI.
## Descripción

Proyecto trabajado durante mi estancia en Nomia Energy
Realizado con el objetivo de crear un cliente capaz de enlazarse la API REST usando el lenguaje Python.

## Tecnología usada

- Python
- requests
- PyCharm
- Git / GitHub
- Swagger UI / OpenAPI
- uv

## Project structure

```text
proyecto-cliente-api/
├── src/
│   └── api_client/
│       ├── __init__.py
│       ├── config.py
│       ├── digital_twin.py
│       └── main.py
├── tests/
├── docs/
├── .gitignore
├── CHANGELOG.md
├── README.md
├── pyproject.toml
└── uv.lock
```

## Installation

1. Clone the repository.
2. Create or activate the virtual environment.
3. Install dependencies.

Example:

```bash
uv sync
```

Or, if needed:

```bash
pip install requests
```

## Usage

Run the project from the source entry point:

```bash
python src/api_client/main.py
```

## Current status

The client currently connects to the local API and consumes the endpoint:

- `GET /api/digital-twin/tree`

## Roadmap

- Improve project structure
- Add reusable request functions
- Learn to interpret Swagger UI/OpenAPI documentation
- Add more endpoints
- Add tests
- Improve error handling and configuration