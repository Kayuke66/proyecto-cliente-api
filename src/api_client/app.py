from fastapi import FastAPI, Request, Body, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.api_client.health import get_health
from src.api_client.system import get_version
from src.api_client.digital_twin import (
    get_devices,
    get_all_points,
    save_digital_twin,
    load_digital_twin,
    import_santra_legacy_json,
    import_ede_from_file,
)

app = FastAPI(title="Santra Web Client - Nomia Energy")

app.mount("/static", StaticFiles(directory="src/api_client/static"), name="static")
templates = Jinja2Templates(directory="src/api_client/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/web-api/health")
def web_health():
    return get_health()


@app.get("/web-api/version")
def web_version():
    return get_version()


@app.get("/web-api/devices")
def web_devices():
    return get_devices()


@app.get("/web-api/points")
def web_points():
    return get_all_points()

@app.post("/web-api/save")
def web_save():
    return save_digital_twin()

@app.post("/web-api/load")
def web_load():
    return load_digital_twin()

@app.post("/web-api/import-santra-json")
def web_import_santra_json(payload: dict = Body(...)):
    resultado = import_santra_legacy_json(payload)
    return {"status": "ok", "data": resultado}

@app.post("/web-api/import-ede")
async def web_import_ede(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(status_code=400, detail="No se ha enviado ningún archivo.")

    try:
        content = await file.read()
    except Exception:
        raise HTTPException(status_code=500, detail="Error al leer el archivo EDE.")

    try:
        resultado = import_ede_from_file(filename=file.filename, content=content)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Error al importar EDE: {exc}")

    return resultado
