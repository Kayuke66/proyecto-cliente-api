# Changelog

Todos los cambios relevantes de este proyecto se documentarán aquí.

El formato está inspirado en Keep a Changelog y el versionado seguirá Semantic Versioning cuando el proyecto quede estabilizado.

## [0.1.0] - 2026-05-18

### Añadido
- Estructura inicial del nuevo proyecto Python/FastAPI.
- Documentación base del proyecto en `README.md`.
- Endpoint inicial planificado: `GET /api/health`.
- Arquitectura por capas inspirada en el proyecto Node original:
  - rutas
  - controlador
  - servicio de health monitor
  - checks independientes
  - schemas Pydantic
- Base de checks de health:
  - `event_loop`
  - `uptime`
  - `memory`
- Preparación para Swagger/OpenAPI automática.
- Archivo `.gitignore` base para entorno Python.
- Archivo `requirements.txt` inicial.

### Cambiado
- Se decide separar el nuevo desarrollo Python del proyecto antiguo para evitar conflictos de imports heredados.
- Se adopta equivalencia funcional con la API Node en lugar de una copia literal del código fuente.

### Corregido
- Identificado el origen del error `ModuleNotFoundError: No module named 'src.api_client'` como dependencia residual del proyecto anterior.

### Pendiente
- Implementación final y validación completa del endpoint `GET /api/health`.
- Añadir tests automáticos.
- Migrar el resto de endpoints.
- Estandarizar respuestas de error.
