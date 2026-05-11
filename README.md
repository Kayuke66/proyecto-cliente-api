# Proyecto Cliente API + Panel Web

Cliente en Python para consumir una API REST y pequeña interfaz web construida con FastAPI, HTML, CSS y JavaScript para visualizar y ejecutar operaciones sobre la API.

## Objetivo del proyecto

Este proyecto empezó como un cliente Python para aprender a consumir una API REST de forma estructurada y modular.  
Después evolucionó hacia una arquitectura con dos capas:

- un cliente Python que encapsula las llamadas HTTP a la API real;
- una aplicación web propia que actúa como backend intermedio y ofrece una interfaz visual.

La idea principal del proyecto es aprender:
- consumo de APIs REST en Python;
- organización modular de un cliente;
- manejo de respuestas JSON y errores;
- construcción de una capa backend propia con FastAPI;
- desarrollo de una interfaz web sencilla con HTML, CSS y JavaScript;
- separación entre frontend, backend propio y API externa.

## Arquitectura actual

La arquitectura del proyecto es:

```text
Frontend (HTML/CSS/JS)
        |
        v
Backend propio (FastAPI)
        |
        v
Cliente Python
        |
        v
API REST real
```

Esto permite que la interfaz web no tenga que hablar directamente con la API externa, sino que lo haga a través del backend Python del proyecto.

## Estructura del proyecto

```text
src/
└── api_client/
    ├── app.py
    ├── client.py
    ├── config.py
    ├── health.py
    ├── system.py
    ├── digital_twin.py
    ├── main.py
    ├── templates/
    │   └── index.html
    └── static/
        ├── styles.css
        └── app.js
```

### Descripción de archivos

- `app.py`: aplicación web FastAPI. Sirve la interfaz HTML y expone rutas `/web-api/...`.
- `client.py`: cliente base para realizar peticiones HTTP a la API real.
- `config.py`: configuración general, como URL base y timeout.
- `health.py`: funciones relacionadas con el endpoint de health.
- `system.py`: funciones relacionadas con información de versión del sistema.
- `digital_twin.py`: funciones relacionadas con árbol, devices, points, save, load e importaciones.
- `main.py`: script de pruebas desde consola.
- `templates/index.html`: plantilla HTML de la interfaz web.
- `static/styles.css`: estilos del frontend, adaptados a la línea visual de Santra.
- `static/app.js`: lógica del frontend, llamadas `fetch`, renderizado de datos y gráfico de health.

## Funcionalidades actuales

### Cliente Python
- Consulta del estado de salud de la API.
- Consulta de la versión del sistema.
- Consulta del árbol del Digital Twin.
- Consulta de dispositivos.
- Consulta de puntos.
- Importación de JSON Santra Legacy.
- Guardado del Digital Twin.
- Carga del Digital Twin.
- Importación de archivo EDE.

### Interfaz web
- Visualización de `Health`.
- Visualización de `Version`.
- Visualización de `Devices` en formato tabla.
- Visualización de `Points` en formato JSON.
- Panel `Health` con métricas resumidas.
- Gráfico interactivo de `Health` con Chart.js.
- Primer flujo preparado para operaciones `POST` desde la web.

## Tecnologías usadas

- Python
- requests
- FastAPI
- Uvicorn
- Jinja2
- HTML
- CSS
- JavaScript
- Chart.js

## Instalación

Crea y activa un entorno virtual, luego instala las dependencias necesarias.

### Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install fastapi requests uvicorn jinja2
```

## Ejecución

### Cliente de consola
```powershell
python src/api_client/main.py
```

### Aplicación web
```powershell
uvicorn src.api_client.app:app --reload
```

Después abre en el navegador:

```text
http://127.0.0.1:8000
```

## Qué hace cada capa

### 1. Cliente Python
Esta capa encapsula la comunicación con la API real.  
Su objetivo es evitar repetir lógica HTTP por todo el proyecto.

Por ejemplo:
- construir URLs;
- enviar peticiones;
- gestionar timeouts;
- convertir respuestas;
- centralizar el acceso a endpoints.

### 2. Backend FastAPI
Esta capa sirve la web y ofrece rutas internas como:

- `/web-api/health`
- `/web-api/version`
- `/web-api/devices`
- `/web-api/points`

Más adelante también podrá exponer rutas `POST` como:
- `/web-api/save`
- `/web-api/load`
- `/web-api/import-santra`

Su función es actuar como intermediario entre el frontend y el cliente Python.

### 3. Frontend
Esta capa es la parte visual.  
Hace peticiones con `fetch()` al backend propio, no directamente a la API externa.

Esto permite:
- ocultar la API real al navegador;
- transformar respuestas;
- controlar errores desde un punto central;
- mantener mejor la seguridad y el diseño de la interfaz.

## Decisiones importantes del diseño

### Paleta visual
Se ha adoptado una línea de color inspirada en Santra:
- fondo oscuro;
- tarjetas en azules oscuros;
- acentos en azul/cian;
- texto claro.

### Visualización de Health
El panel `Health` muestra:
- estado;
- uptime;
- delay;
- memoria RSS;
- detalles adicionales;
- gráfico interactivo.

La idea no es solo mostrar JSON en bruto, sino traducir parte de la respuesta a una interfaz más útil visualmente.

## Problemas resueltos durante el desarrollo

### 1. Imports en módulos
Se corrigieron imports para usar la ruta consistente `src.api_client...`.

### 2. TemplateResponse
Se actualizó la sintaxis para usar:
```python
templates.TemplateResponse(request=request, name="index.html")
```

### 3. Dependencias faltantes
Se instalaron:
- fastapi
- requests
- uvicorn
- jinja2

### 4. Ajustes visuales
Se corrigieron problemas de CSS, espaciado y maquetación de la interfaz.

## Próximos pasos previstos

- Añadir `POST /web-api/save` funcional desde la interfaz.
- Añadir `POST /web-api/load`.
- Crear formulario visual para importación de JSON Santra Legacy.
- Estudiar subida de archivos EDE desde la web.
- Mejorar el tratamiento visual de errores.
- Refinar el README, el changelog y el versionado en cada avance importante.

## Notas de aprendizaje

Este proyecto no busca solo “hacer que funcione”, sino entender qué hace cada pieza.  
Por eso se ha construido paso a paso:
- primero el cliente Python;
- luego la organización modular;
- después el backend FastAPI;
- y finalmente la capa visual.

## Versionado

Este proyecto sigue Semantic Versioning en formato:

```text
MAJOR.MINOR.PATCH
```

Regla práctica usada en este proyecto:
- `PATCH`: correcciones y pequeños ajustes.
- `MINOR`: nuevas funcionalidades compatibles.
- `MAJOR`: cambios grandes o incompatibles.

Versión actual propuesta:

```text
0.3.0
```

## Changelog

Consulta `CHANGELOG.md` para ver el historial de cambios del proyecto.