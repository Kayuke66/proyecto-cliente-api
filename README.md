# Santra API Client (Python)

Cliente/API en Python con FastAPI que replica progresivamente el comportamiento de la API original de Santra Edge Agent, con foco actual en el módulo **Digital Twin**.

## Estado actual

A fecha de esta actualización, el proyecto ya tiene una base funcional con FastAPI, middlewares globales, manejo centralizado de errores, documentación OpenAPI personalizada y una implementación amplia del dominio Digital Twin.[web:1098]

También se ha añadido persistencia local del Digital Twin para conservar devices, points y tree tras refrescar la aplicación o reiniciar el proceso, alineando el comportamiento con la versión original basada en persistencia al arranque y guardado tras importaciones.[web:1403]

## Funcionalidades implementadas

### Infraestructura base

- Aplicación FastAPI con `app.py` como punto de entrada.
- Middlewares comunes y CORS ajustado.
- Eliminado `Access-Control-Expose-Headers` de las respuestas CORS al retirar `expose_headers` del middleware.[web:1189]
- Gestión centralizada de errores con `SantraError` y catálogo de errores.
- OpenAPI/Swagger personalizado con examples y responses afinadas en varios endpoints.[web:1098]

### Digital Twin

#### GET implementados/corregidos

- `GET /api/digital-twin/tree`
- `GET /api/digital-twin/devices`
- `GET /api/digital-twin/devices/{id}`
- `GET /api/digital-twin/points`
- `GET /api/digital-twin/devices/{id}/points`
- `GET /api/digital-twin/equipments/{id}/points`

#### Ajustes relevantes realizados

- Normalización de `description` y `unit` a `""` cuando el original no devuelve `null`, evitando errores de validación de Pydantic en responses.[web:1377]
- Ajuste de `unitId` para devolver valor numérico por defecto (`0`) en lugar de `null` cuando aplica.
- Corrección de serialización de devices para incluir `host`, `port` y `unitId` en responses.
- Exclusión de campos `None` en el árbol (`response_model_exclude_none=True`) para eliminar `metadata: null` y acercar la salida al formato de la API original.[web:1404]
- Corrección de `create_device()` y `create_point()` para usar modelos reales en lugar de objetos dinámicos ad hoc.
- Corrección de persistencia de jerarquía por punto para que el tree no salga vacío.

### Importaciones

#### `POST /api/digital-twin/import/ede`

Implementado con:

- parser de EDE
- validador
- intérprete
- resolver de estructura
- catálogo/resolver BACnet
- persistencia inmediata tras importación

Se ajustó además la documentación Swagger para mostrar un ejemplo realista en `text/plain` en lugar de `"string"`, usando ejemplos de body en FastAPI/OpenAPI.[web:1342]

#### `POST /api/digital-twin/import/santra-legacy-json`

Trabajo preparado y ya documentado a nivel de arquitectura, con piezas identificadas para:

- parser de legacy JSON
- intérprete principal
- estrategias BACnet y Modbus
- DTO de respuesta
- integración con persistencia

Queda pendiente cerrar la implementación final en código y probarla extremo a extremo.

## Persistencia

La versión Python ya no depende solo de memoria en runtime. Se ha introducido una capa de persistencia local para:

- guardar el Digital Twin tras importaciones
- cargar el estado persistido en el arranque mediante `lifespan`
- mantener datos tras F5 o reinicio del proceso

FastAPI soporta inicialización al arranque mediante lifespan/events, que es la base recomendada para este patrón.[web:1403][web:1395]

## Estructura orientativa

```text
src/
├── api/
│   └── routes/
├── core/
│   ├── errors/
│   └── ...
├── schemas/
├── services/
│   ├── ingestion/
│   │   ├── ede/
│   │   └── santra_legacy/
│   ├── protocols/
│   │   ├── bacnet/
│   │   └── modbus/
│   ├── digital_twin_service.py
│   ├── digital_twin_store.py
│   ├── digital_twin_models.py
│   └── persistence_service.py
└── app.py
```

## Pendiente inmediato

- Cerrar `POST /api/digital-twin/import/santra-legacy-json` en Python.
- Retomar los POST restantes del módulo Digital Twin.
- Revisar endpoint a endpoint la fidelidad con la API original en responses, examples y errores.
- Añadir tests automáticos para imports y serialización.

## Ejecución local

Comandos típicos:

```bash
uvicorn src.app:app --reload
```

o, según tu estructura real:

```bash
uvicorn app:app --reload
```

## Git

Flujo básico para subir cambios:

```bash
git status
git add .
git commit -m "docs: update README and CHANGELOG for digital twin progress"
git push origin <tu-rama>
```

Si aún no has creado rama de trabajo:

```bash
git checkout -b feature/digital-twin-sync
```

## Nota técnica

Si en `digital_twin_service.py` aparecen subrayados en rojo `SantraError` y `ERRORS`, faltan imports explícitos del modelo y del catálogo de errores. Eso es coherente con el uso que se hace en `import_santra_legacy_json()` y en otros flujos de importación.[file:1237]
