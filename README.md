# SANTRA Python API

Reimplementación en Python/FastAPI del backend original en Node.js/Express para el módulo de Digital Twin,
manteniendo la equivalencia funcional de los endpoints, la separación por capas y la documentación OpenAPI.

## Descripción

Este proyecto traslada a Python la lógica principal del servicio original, adaptando su arquitectura al 
ecosistema FastAPI sin perder el comportamiento esperado del backend fuente. El objetivo no ha sido copiar literalmente 
el código TypeScript, sino reconstruir sus contratos, respuestas, flujo de persistencia y organización interna de forma 
idiomática en Python.

La migración se ha centrado especialmente en:

- endpoint de health del sistema
- endpoint de versión
- endpoints del dominio Digital Twin
- persistencia del estado del Digital Twin
- documentación Swagger/OpenAPI adaptada
- manejo coherente de errores mediante excepciones de dominio

## Objetivo del proyecto

Los objetivos principales han sido:

- construir una API Python autónoma y desacoplada del proyecto cliente anterior
- mantener equivalencia funcional con la API original
- conservar una arquitectura limpia por capas: rutas, controladores, servicios y persistencia
- documentar los endpoints en Swagger con ejemplos y respuestas útiles
- dejar una base mantenible para revisar y completar diferencias con el proyecto original

## Alcance funcional completado

A nivel de migración, el proyecto ha quedado preparado o implementado con esta cobertura funcional:

- `GET /api/health`
- `GET /api/version`
- endpoints de lectura del Digital Twin
- endpoints de consulta de devices y points
- `POST /api/digital-twin/save`
- `POST /api/digital-twin/load`
- respuestas JSON alineadas con el contrato funcional esperado
- documentación OpenAPI/Swagger ajustada para mostrar las responses relevantes

## Arquitectura

La API se ha diseñado con una estructura inspirada en el proyecto original, pero adaptada a FastAPI y Python:

- **routes**: definición de endpoints HTTP y metadatos OpenAPI
- **controllers / handlers**: capa de entrada cuando aplica, orientada a mantener claridad de responsabilidades
- **services**: lógica principal de negocio
- **persistence**: guardado y carga del estado del Digital Twin
- **schemas / dto**: modelos Pydantic para request/response cuando interesa documentar o validar
- **errors**: errores de dominio y catálogo de errores

Esta separación permite mantener el comportamiento del backend original con una organización más predecible
y fácil de exponer en revisión técnica.

## Comportamiento del Digital Twin

El módulo Digital Twin es el núcleo del proyecto.

Su funcionamiento general es:

1. La API expone endpoints para consultar el estado del Digital Twin, devices y points.
2. El servicio central mantiene el estado del modelo en memoria.
3. La capa de persistencia permite guardar ese estado de forma explícita mediante `save`.
4. El endpoint `load` recupera desde persistencia el modelo previamente almacenado y reemplaza el estado actual en memoria.
5. Ante fallos de persistencia, el servicio transforma la excepción en un error de dominio consistente.

### Save

El endpoint de guardado:

- no requiere body
- ejecuta la operación de persistencia del modelo actual
- devuelve `201 Created`
- responde con:

```json
{
  "status": "ok"
}
```

### Load

El endpoint de carga:

- no requiere body
- recupera el estado del Digital Twin desde persistencia
- sustituye el modelo actual en memoria por el cargado
- devuelve `200 OK`
- responde con:

```json
{
  "status": "ok"
}
```

## Documentación OpenAPI

Se ha trabajado la documentación Swagger para que refleje correctamente el comportamiento útil de la API
sin sobrecargar innecesariamente la vista de schemas.

Entre los ajustes realizados:

- definición explícita de respuestas por endpoint
- ejemplos de respuestas JSON donde aporta valor
- control de visibilidad de schemas en endpoints simples como `save` y `load`
- adaptación de modelos de respuesta para que la documentación sea más clara para consumo y revisión

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

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Desde la raíz del proyecto, arrancar la aplicación con Uvicorn usando el módulo donde esté declarada la app FastAPI. 
Un ejemplo habitual sería:

```bash
uvicorn src.app:app --reload
```

Si la aplicación principal está en otro archivo, debe sustituirse esa ruta por la real del proyecto.

## Uso y verificación

### Swagger

Abrir en navegador:

- `http://127.0.0.1:8000/docs`

### Comprobaciones recomendadas

- verificar `GET /api/health`
- verificar `GET /api/version`
- revisar en Swagger los endpoints del dominio Digital Twin
- comprobar persistencia con `POST /api/digital-twin/save`
- reinicializar o alterar el estado en memoria si procede
- recuperar el estado con `POST /api/digital-twin/load`

## Equivalencia con el proyecto original

La migración ha seguido una estrategia de equivalencia funcional:

- mismas responsabilidades por capa
- mismo flujo general de guardado y carga
- respuestas HTTP alineadas con el backend original
- adaptación de DTOs TypeScript a modelos Pydantic cuando tiene sentido
- diferencias mínimas debidas al runtime Python/FastAPI frente a Node/Express

En otras palabras, se ha priorizado reproducir el comportamiento observable y la intención del sistema original 
que clonar literalmente su implementación.

## Estado final

En este punto el proyecto queda en un estado válido para:

- revisión funcional
- demostración ante supervisor
- comparación final contra el proyecto original
- identificación de endpoints o detalles menores aún no migrados

## Próximo paso recomendado

El siguiente trabajo lógico es hacer una revisión comparativa final contra el backend original para detectar:

- endpoints no migrados
- diferencias menores en documentación o códigos de respuesta
- campos opcionales pendientes
- detalles de persistencia o errores de dominio aún mejorables
