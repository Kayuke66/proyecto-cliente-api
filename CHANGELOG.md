# Changelog

## Unreleased

### Added

- Persistencia local del Digital Twin mediante servicio dedicado.
- Carga del estado persistido al arrancar la aplicación usando lifespan.
- Modelos reales `Device` y `Point` para el store del Digital Twin.
- Base de implementación para importación de EDE.
- Base de implementación/documentación para importación de Santra Legacy JSON.

### Changed

- Ajustadas responses de endpoints de Digital Twin para alinearlas con la API original.
- `GET /api/digital-twin/tree` ahora excluye campos `None` en la respuesta para evitar `metadata: null`.[web:1404]
- `GET /api/digital-twin/devices` y `GET /api/digital-twin/devices/{id}` actualizados para incluir `host`, `port` y `unitId`.
- `unitId` normalizado a valor numérico por defecto cuando no existe.
- Normalización de `description` y `unit` a cadena vacía en DTOs de points para evitar errores de validación de Pydantic.[web:1377]
- Documentación OpenAPI mejorada con examples reales en body y responses en varios endpoints.[web:1098]
- Eliminado `Access-Control-Expose-Headers` de respuestas CORS al retirar `expose_headers` del middleware.[web:1189]

### Fixed

- Error 500 por falta de `siteId` en la response real de `import ede` cuando el `response_model` lo requería.[web:1098]
- Error 500 en tree por `description=None` en `CompactPointDto`.[web:1377]
- Árbol vacío por persistencia incorrecta de jerarquía de puntos en el store.
- Error 500 en `get all points for a device` por `unit=None` en `PointDto`.[web:1377]
- Desalineación entre respuesta real y example value en documentación Swagger/OpenAPI.[web:1098]

### Pending

- Implementación final y validación de `POST /api/digital-twin/import/santra-legacy-json`.
- Continuación de los POST restantes del módulo Digital Twin.
- Revisión de tests y cobertura.
