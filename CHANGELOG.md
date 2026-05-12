# Changelog

Este proyecto sigue una convención inspirada en Keep a Changelog y Semantic Versioning.

## [0.3.1] - 2026-05-12

### Added
- Añadido flujo completo de importación Santra Legacy JSON desde la interfaz web.

## [0.3.0] - 2026-05-11

### Added
- Se añadió una aplicación web con FastAPI como backend intermedio.
- Se añadieron plantillas HTML con Jinja2.
- Se añadieron archivos estáticos para CSS y JavaScript.
- Se añadió una interfaz visual inicial para consultar Health, Version, Devices y Points.
- Se añadió una tabla HTML dinámica para visualizar Devices.
- Se añadió un panel visual de Health con métricas resumidas.
- Se añadió soporte para gráficos interactivos con Chart.js en el panel de Health.
- Se preparó la base para ejecutar operaciones POST desde la interfaz web.
- Se adoptó una línea visual inspirada en la identidad de color de Santra.

### Changed
- Se reorganizó el proyecto para trabajar con una arquitectura frontend + backend Python + cliente API.
- Se actualizaron los imports internos a la convención `src.api_client...`.
- Se actualizó la forma de renderizar plantillas en FastAPI con `TemplateResponse(request=request, name="index.html")`.
- Se mejoró la presentación visual del panel principal.
- Se mejoró la estructura del frontend para separar bloques de resumen, tablas y paneles de detalle.

### Fixed
- Se corrigieron errores de importación que impedían ejecutar `uvicorn`.
- Se corrigieron dependencias faltantes para FastAPI, Uvicorn, Jinja2 y requests.
- Se corrigieron problemas de maquetación y estilos en la interfaz web.
- Se corrigió el problema de carga y actualización del gráfico de Health.

## [0.2.0] - 2026-05-08

### Added
- Se añadió una estructura modular inicial para el cliente Python.
- Se añadieron funciones para consultar Health, Version, Devices, Points y árbol del Digital Twin.
- Se añadieron funciones para Save, Load, importación de JSON Santra Legacy e importación de EDE.
- Se añadió un script principal de pruebas desde consola.

### Changed
- Se separó la lógica por módulos para facilitar mantenimiento y comprensión.
- Se mejoró la legibilidad del flujo de pruebas del cliente.

### Fixed
- Se ajustaron respuestas y validaciones al comportamiento observado en Swagger.

## [0.1.0] - 2026-05-07

### Added
- Inicio del proyecto como cliente Python para consumir una API REST.
- Configuración base del cliente HTTP.
- Primeras pruebas manuales con endpoints GET.