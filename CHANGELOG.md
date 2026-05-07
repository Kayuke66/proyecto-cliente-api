# Changelog
Los cambios de este proyecto están documentados en este archivo.

Formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

## [0.2.0] - 2026-05-07
### Añadido
- Cliente base reutilizable para realizar peticiones `GET` a la API.
- Módulo `health` para consumir `GET /api/health`.
- Módulo `system` para consumir `GET /api/version`.
- Ampliación del módulo `digital_twin` con varios endpoints `GET`.
- Organización del proyecto en módulos bajo `src/api_client/`.

### Cambiado
- Separación de la lógica de ejecución en `main.py`.
- Reestructuración del proyecto hacia un formato más profesional y mantenible.

### Corregido
- Uso incorrecto de `raise_for_status()`.
- Problemas iniciales de imports y estructura del proyecto.
- Error de indentación en la clase `APIClient`.
- Orden de las excepciones `except` para evitar código inalcanzable.


## [0.1.0] - 2026-05-07

### Añadido
- Estructura inicial del proyecto profesional. 
- Cliente API base con lógica GET reutilizable.
- Consumo inicial del punto final Digital Twin.
- Integración de README, CHANGELOG y Git.
