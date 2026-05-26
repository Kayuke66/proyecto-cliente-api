# Changelog

Todos los cambios relevantes de este proyecto se documentan aquí.

El formato está inspirado en Keep a Changelog. El versionado podrá ajustarse más adelante cuando el proyecto entre en fase de estabilización completa.

## [1.0.0] - 2026-05-26

### Añadido
- Reimplementación en Python/FastAPI del backend base originalmente desarrollado en Node.js/Express.
- Documentación definitiva del proyecto en `README.md`.
- Base de dependencias del proyecto en `requirements.txt`.
- Endpoint `GET /api/health` con estructura equivalente a la del sistema original.
- Endpoint `GET /api/version`.
- Migración del dominio principal de Digital Twin.
- Endpoints de consulta para Digital Twin, devices y points.
- Endpoint `POST /api/digital-twin/save`.
- Endpoint `POST /api/digital-twin/load`.
- Soporte de persistencia para guardado y carga del estado del Digital Twin.
- Respuestas JSON simples y consistentes para operaciones de save/load.
- Base de errores de dominio para fallos de persistencia.
- Documentación Swagger/OpenAPI ajustada para mostrar las responses relevantes de cada endpoint.

### Cambiado
- Se consolida la migración como proyecto Python autónomo, separado del cliente anterior y de dependencias residuales heredadas.
- Se adopta FastAPI como framework principal para reemplazar la capa HTTP del backend Node original.
- Se adapta la documentación OpenAPI para priorizar claridad en responses y reducir ruido visual en schemas de endpoints simples.
- Se mantiene equivalencia funcional con el sistema original, traduciendo la implementación a convenciones idiomáticas de Python.

### Corregido
- Resolución de problemas iniciales derivados de imports y estructura heredada del proyecto previo.
- Ajustes en documentación Swagger para evitar exposición innecesaria de schemas en endpoints simples.
- Verificación funcional del flujo `save`/`load` del Digital Twin.

### Estado
- Proyecto listo para revisión final frente al backend original.
- Base preparada para detectar y completar posibles diferencias menores restantes.
