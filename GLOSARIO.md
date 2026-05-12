# Glosario del proyecto

Glosario de términos utilizados durante el desarrollo del cliente API y del panel web.  
Está organizado por tecnologías y lenguajes para facilitar el estudio.

---

# Python

## Python
Lenguaje principal del proyecto.  
Se usa para construir el cliente de la API, la lógica backend y la aplicación web con FastAPI.

## requests
Librería de Python para hacer peticiones HTTP.  
Permite enviar `GET`, `POST`, `PUT`, `DELETE`, headers, parámetros y cuerpos JSON.

## import
Palabra clave de Python para importar módulos, funciones o clases desde otros archivos o paquetes.

## módulo
Archivo `.py` que contiene código reutilizable.  
En este proyecto, por ejemplo: `health.py`, `system.py`, `digital_twin.py`.

## paquete
Conjunto de módulos agrupados dentro de una carpeta Python.  
En este proyecto, `src.api_client` actúa como paquete principal.

## función
Bloque de código reutilizable definido con `def`.  
Ejemplo: `get_health()` o `save_digital_twin()`.

## clase
Estructura que agrupa datos y comportamientos.  
En este proyecto se usa, por ejemplo, en el cliente base `APIClient`.

## instancia
Objeto concreto creado a partir de una clase.  
Si haces `client = APIClient()`, `client` es una instancia.

## argumento
Valor que se pasa a una función o método al llamarlo.

## parámetro
Nombre que aparece en la definición de una función para recibir valores.

## return
Palabra clave que devuelve un resultado desde una función.

## diccionario
Estructura clave-valor de Python, parecida a un objeto JSON.  
Se escribe con llaves: `{}`.

## lista
Colección ordenada de elementos en Python.  
Se escribe con corchetes: `[]`.

## excepción
Error que ocurre durante la ejecución del programa.  
Se puede capturar con `try/except`.

## try / except
Estructura para controlar errores sin romper completamente el programa.

## timeout
Tiempo máximo de espera para una petición HTTP.  
Evita que el programa se quede esperando indefinidamente.

## virtualenv / venv
Entorno virtual de Python.  
Permite instalar dependencias solo para este proyecto.

## pip
Gestor de paquetes de Python.  
Se usa para instalar librerías como `requests`, `fastapi` o `jinja2`.

## main.py
Archivo principal de ejecución en consola para pruebas manuales del cliente.

## client.py
Archivo que encapsula la lógica base de comunicación HTTP con la API.

## config.py
Archivo de configuración del proyecto.  
Suele contener URL base, timeouts y constantes.

---

# FastAPI y backend web

## FastAPI
Framework web para Python.  
Se usa para crear rutas HTTP, servir JSON y montar la aplicación web.

## app = FastAPI()
Instancia principal de la aplicación.  
Desde ella se definen rutas, configuración y recursos estáticos.

## endpoint
Ruta concreta de una API.  
Ejemplo: `/web-api/health`.

## ruta
Camino HTTP que responde a una petición del cliente o del navegador.

## @app.get(...)
Decorador que define una ruta HTTP de tipo GET.

## @app.post(...)
Decorador que define una ruta HTTP de tipo POST.

## decorador
Sintaxis especial de Python con `@` que modifica o registra una función.  
En FastAPI sirve para indicar qué función responde a cada ruta.

## Request
Objeto que representa la petición entrante en FastAPI.

## Response
Objeto de respuesta HTTP.  
Puede ser HTML, JSON u otro tipo de contenido.

## HTMLResponse
Tipo de respuesta HTML en FastAPI.

## Jinja2Templates
Sistema de plantillas HTML usado por FastAPI para renderizar páginas.

## TemplateResponse
Respuesta que devuelve una plantilla HTML renderizada con datos.

## StaticFiles
Componente de FastAPI para servir archivos estáticos como CSS y JS.

## uvicorn
Servidor ASGI que ejecuta la app FastAPI.

## ASGI
Interfaz moderna para aplicaciones web Python, sucesora conceptual de WSGI.

## backend
Parte del sistema que corre en el servidor y maneja lógica, datos y comunicación con otras APIs.

## middleware
Capa intermedia que procesa peticiones o respuestas.  
No la estamos usando todavía, pero es importante conocerla.

---

# JavaScript

## JavaScript
Lenguaje que corre en el navegador.  
En este proyecto gestiona la interacción del frontend con el backend FastAPI.

## fetch
API de JavaScript para hacer peticiones HTTP desde el navegador.

## async
Palabra clave para declarar una función asíncrona.

## await
Palabra clave que espera el resultado de una promesa dentro de una función `async`.

## promesa
Objeto de JavaScript que representa un valor futuro que llegará cuando una operación asíncrona termine.

## addEventListener
Método para escuchar eventos del navegador, como clics en botones.

## click
Evento que se dispara al pulsar un botón u otro elemento interactivo.

## DOM
Modelo de objetos del documento HTML.  
Representa la página como una estructura manipulable desde JavaScript.

## document.getElementById(...)
Método para obtener un elemento HTML por su `id`.

## innerHTML
Propiedad que permite insertar HTML dentro de un elemento.

## textContent
Propiedad que inserta texto plano dentro de un elemento.

## JSON.stringify(...)
Convierte un objeto JavaScript en texto JSON.

## response.ok
Propiedad que indica si la respuesta HTTP fue correcta.

## setInterval
Función de JavaScript para repetir una acción periódicamente.  
Se valoró para refrescar Health, aunque se decidió no usarla por ahora.

## Chart.js
Librería JavaScript para crear gráficos interactivos en canvas.

## chart
Objeto gráfico que representa datos de forma visual.

## canvas
Elemento HTML donde se dibujan gráficos o dibujos con JavaScript.

## destroy()
Método usado para destruir un gráfico anterior antes de crear otro nuevo sobre el mismo canvas.

---

# HTML

## HTML
Lenguaje de marcado que define la estructura de la página web.

## etiqueta
Elemento HTML como `<div>`, `<section>`, `<button>` o `<pre>`.

## atributo
Propiedad dentro de una etiqueta HTML.  
Ejemplo: `id="btn-health"`.

## id
Identificador único de un elemento HTML.

## class
Nombre de clase CSS aplicado a uno o varios elementos HTML.

## `<main>`
Contenedor principal del contenido de la página.

## `<section>`
Bloque semántico para agrupar contenido relacionado.

## `<article>`
Bloque semántico para contenido independiente o con sentido propio.

## `<header>`
Cabecera de una página o sección.

## `<button>`
Botón interactivo.

## `<pre>`
Elemento HTML que conserva espacios y saltos de línea.  
Muy útil para mostrar JSON formateado.

## `<table>`
Tabla HTML para mostrar datos estructurados.

## `<thead>`
Cabecera de la tabla.

## `<tbody>`
Cuerpo de la tabla.

## `<tr>`
Fila de una tabla.

## `<th>`
Celda de cabecera de tabla.

## `<td>`
Celda de datos de tabla.

## plantilla
HTML base que luego puede renderizarse con datos desde el backend.

---

# CSS

## CSS
Lenguaje de estilos usado para definir la apariencia visual de la web.

## selector
Parte del CSS que indica a qué elementos se aplica una regla.  
Ejemplo: `body`, `.card`, `#health-summary`.

## propiedad
Característica visual que se modifica en CSS.  
Ejemplo: `color`, `padding`, `margin`.

## valor
Contenido asignado a una propiedad CSS.  
Ejemplo: `color: white;`.

## margin
Espacio exterior alrededor de un elemento.

## padding
Espacio interior entre el contenido y el borde del elemento.

## border
Borde de un elemento.

## border-radius
Redondeado de esquinas.

## box-shadow
Sombra visual de un elemento.

## display
Propiedad que define cómo se comporta un elemento en el layout.

## grid
Sistema de maquetación bidimensional de CSS.  
Se usa para organizar columnas y tarjetas.

## flex
Sistema flexible de distribución de elementos en una fila o columna.

## gap
Espacio entre elementos dentro de un contenedor `grid` o `flex`.

## media query
Regla CSS para adaptar la web a diferentes tamaños de pantalla.

## responsive
Diseño que se adapta a móvil, tablet y escritorio.

## variable CSS
Valor reutilizable definido normalmente en `:root`, como `--color-primary`.

---

# JSON

## JSON
Formato de intercambio de datos muy usado en APIs.  
Se parece a un diccionario de Python y a un objeto de JavaScript.

## clave
Nombre de un campo dentro de un objeto JSON.

## valor
Dato asociado a una clave.

## objeto JSON
Estructura de pares clave-valor delimitada por llaves.

## array JSON
Lista ordenada de valores delimitada por corchetes.

## serializar
Convertir un objeto en texto JSON.

## deserializar
Convertir texto JSON en una estructura utilizable por el programa.

## body
Contenido de la petición o respuesta HTTP.  
Muchas APIs envían y reciben JSON en el body.

---

# HTTP y APIs

## API
Interfaz de programación que permite que un sistema hable con otro.

## API REST
Estilo de API basado en recursos y métodos HTTP.

## recurso
Entidad sobre la que opera la API.  
Ejemplo: `devices`, `points`, `health`.

## URL
Dirección de un recurso.

## endpoint
URL concreta de un recurso o acción de la API.

## GET
Método HTTP para consultar datos.

## POST
Método HTTP para enviar datos o ejecutar acciones.

## PUT
Método HTTP para actualizar completamente un recurso.

## PATCH
Método HTTP para actualizar parcialmente un recurso.

## DELETE
Método HTTP para eliminar un recurso.

## header
Metadato de la petición o la respuesta.  
Ejemplo: `Content-Type: application/json`.

## Content-Type
Header que indica el tipo de contenido enviado.

## status code
Código numérico de respuesta HTTP.  
Ejemplo: `200`, `404`, `500`.

## response
Respuesta devuelta por un servidor.

## request
Petición enviada por un cliente.

## timeout
Tiempo límite de espera para una operación HTTP.

## health
Endpoint o concepto de monitorización usado para saber si un servicio está funcionando correctamente.

## uptime
Tiempo que lleva activo un proceso o servicio desde que se arrancó.

## delayMs
Retardo medido en milisegundos, normalmente asociado a latencia o al event loop.

---

# Git y GitHub

## Git
Sistema de control de versiones.

## GitHub
Plataforma para alojar repositorios Git y gestionar releases, issues y colaboración.

## repositorio
Carpeta controlada por Git con historial de cambios.

## branch
Rama de desarrollo.

## main
Rama principal del proyecto en muchos repositorios.

## commit
Registro de un conjunto de cambios en el historial Git.

## staging
Área intermedia donde se preparan cambios antes del commit.

## git add
Comando para añadir archivos al staging.

## git commit
Comando para guardar cambios en el historial del repositorio.

## git push
Comando para subir commits o tags al remoto.

## remoto
Repositorio alojado en un servidor, como GitHub.

## tag
Etiqueta fija asociada a un commit concreto.  
Se usa para marcar versiones como `v0.3.0`.

## release
Publicación formal de una versión del proyecto, normalmente basada en un tag.

## Semantic Versioning
Sistema de versionado `MAJOR.MINOR.PATCH`.  
En este proyecto se usa para organizar la evolución funcional.

## changelog
Archivo que documenta cambios por versión.

## README
Archivo principal de documentación del proyecto.

---

# Linux, terminal y comandos

## terminal
Interfaz de texto para ejecutar comandos.

## shell
Programa que interpreta comandos en terminal.

## PowerShell
Shell habitual en Windows.  
Es el entorno que estás usando en tus ejemplos.

## comando
Instrucción escrita en terminal.

## ruta
Ubicación de un archivo o carpeta en el sistema.

## directorio
Carpeta del sistema de archivos.

## cd
Comando para cambiar de directorio.

## ls
Comando para listar archivos en Linux/macOS.

## dir
Comando equivalente a `ls` en Windows CMD.

## mkdir
Comando para crear carpetas.

## archivo estático
Archivo servido tal cual por el backend, como CSS, JS o imágenes.

## proceso
Programa en ejecución.

## entorno virtual
Entorno aislado para dependencias Python.

---

# Arquitectura y diseño del proyecto

## frontend
Parte visual con la que interactúa el usuario.  
En este proyecto usa HTML, CSS y JavaScript.

## backend
Parte que corre en el servidor y concentra la lógica de acceso a datos y APIs.

## cliente API
Capa Python que encapsula llamadas a la API real.

## fachada
Patrón donde una capa simplifica el acceso a otra más compleja.

## Backend for Frontend
Patrón en el que el frontend no habla directamente con servicios externos, sino con un backend propio adaptado a sus necesidades.

## separación de responsabilidades
Idea de dividir el sistema en capas con roles claros.

## modularidad
Diseño en piezas separadas para facilitar mantenimiento y comprensión.

## refactorización
Cambio interno del código para mejorar estructura sin cambiar su comportamiento externo.

## visualización
Forma de representar datos de manera comprensible en la interfaz.

## dashboard
Panel visual que muestra métricas, estados y acciones del sistema.

## Santra Legacy
Formato o bloque funcional del proyecto relacionado con la importación de datos JSON específicos de Santra.

## Digital Twin
Conjunto de recursos y operaciones del dominio funcional con los que estás trabajando en la API.