let healthChartInstance = null;

async function obtenerDatos(url) {
    const response = await fetch(url);

    if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
    }

    return await response.json();
}

async function enviarPost(url, body) {
    const response = await fetch (url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body),
    });

    if (!response.ok) {
        const text = await response.text();
        throw new Error(`Error ${response.status} - ${text}`);
    }

    return response.json();
}

function destruirHealthChartSiExiste() {
    if (healthChartInstance) {
        healthChartInstance.destroy();
        healthChartInstance = null;
    }
}

function renderHealthChart(delayMs, rssMb, heapUsedMb, heapTotalMb) {
    const canvas = document.getElementById("healthChart");

    if (!canvas) {
        return;
    }

    const ctx = canvas.getContext("2d");

    destruirHealthChartSiExiste();

    healthChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Delay (ms)", "RSS (MB)", "Heap Used (MB)", "Heap Total (MB)"],
            datasets: [{
                label: "Métricas de Health",
                data: [delayMs, rssMb, heapUsedMb, heapTotalMb],
                backgroundColor: [
                    "#00a8ff",
                    "#7dd3fc",
                    "#38bdf8",
                    "#60a5fa"
                ],
                borderColor: "#0ea5e9",
                borderWidth: 1,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: "#f3f4f6"
                    }
                },
                tooltip: {
                    enabled: true
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: "#cbd5e1"
                    },
                    grid: {
                        color: "#334155"
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: "#cbd5e1"
                    },
                    grid: {
                        color: "#334155"
                    }
                }
            }
        }
    });
}

function renderHealth(data) {
    const status = data.status ?? "desconocido";
    const uptime = data.checks?.uptime?.meta?.uptimeFormatted ?? "sin datos";
    const delayMs = data.checks?.event_loop?.meta?.delayMs ?? "sin datos";
    const rssMb = data.checks?.memory?.meta?.rssMb ?? "sin datos";
    const heapUsedMb = data.checks?.memory?.meta?.heapUsedMb ?? 0;
    const heapTotalMb = data.checks?.memory?.meta?.heapTotalMb ?? 0;
    const startedAt = data.checks?.uptime?.meta?.startedAt ?? "sin datos";

    const statusElement = document.getElementById("health-status");
    const uptimeElement = document.getElementById("health-uptime");
    const delayElement = document.getElementById("health-delay");
    const rssElement = document.getElementById("health-rss");
    const detailsElement = document.getElementById("health-details");

    if (statusElement) {
        statusElement.textContent = status;
        statusElement.className = `kpi-value ${status === "ok" ? "status-ok" : "status-warning"}`;
    }

    if (uptimeElement) {
        uptimeElement.textContent = uptime;
    }

    if (delayElement) {
        delayElement.textContent = `${delayMs} ms`;
    }

    if (rssElement) {
        rssElement.textContent = `${rssMb} MB`;
    }

    if (detailsElement) {
        detailsElement.innerHTML = `
            <p><strong>Started at:</strong> ${startedAt}</p>
            <p><strong>Heap used:</strong> ${heapUsedMb} MB</p>
            <p><strong>Heap total:</strong> ${heapTotalMb} MB</p>
        `;
    }

    renderHealthChart(
        Number(delayMs) || 0,
        Number(rssMb) || 0,
        Number(heapUsedMb) || 0,
        Number(heapTotalMb) || 0
    );
}

function renderVersion(data) {
    const target = document.getElementById("version-summary");

    if (!target) {
        return;
    }

    target.innerHTML = `
        <p><strong>Nombre:</strong> ${data.name ?? "sin datos"}</p>
        <p><strong>Versión:</strong> ${data.version ?? "sin datos"}</p>
        <p><strong>Build:</strong> ${data.build ?? "sin datos"}</p>
    `;
}

function renderDevicesTable(devices) {
    const target = document.getElementById("devices-result");

    if (!target) {
        return;
    }

    if (!Array.isArray(devices) || devices.length === 0) {
        target.innerHTML = `<div class="empty-state">No hay dispositivos disponibles.</div>`;
        return;
    }

    const headers = ["id", "name", "description", "protocol", "host", "port", "unitId"];

    const thead = headers.map(header => `<th>${header}</th>`).join("");
    const tbody = devices.map(device => `
        <tr>
            ${headers.map(header => `<td>${device[header] ?? ""}</td>`).join("")}
        </tr>
    `).join("");

    target.innerHTML = `
        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>${thead}</tr>
                </thead>
                <tbody>
                    ${tbody}
                </tbody>
            </table>
        </div>
    `;
}

async function cargarHealth() {
    const details = document.getElementById("health-details");

    if (details) {
        details.textContent = "Cargando...";
    }

    try {
        const data = await obtenerDatos("/web-api/health");
        renderHealth(data);
    } catch (error) {
        if (details) {
            details.textContent = error.message;
        }
        destruirHealthChartSiExiste();
    }
}

async function cargarVersion() {
    const target = document.getElementById("version-summary");

    if (target) {
        target.textContent = "Cargando...";
    }

    try {
        const data = await obtenerDatos("/web-api/version");
        renderVersion(data);
    } catch (error) {
        if (target) {
            target.textContent = error.message;
        }
    }
}

async function cargarDevices() {
    const target = document.getElementById("devices-result");

    if (target) {
        target.innerHTML = `<div class="empty-state">Cargando...</div>`;
    }

    try {
        const data = await obtenerDatos("/web-api/devices");
        renderDevicesTable(data);
    } catch (error) {
        if (target) {
            target.innerHTML = `<div class="empty-state">${error.message}</div>`;
        }
    }
}

async function cargarPoints() {
    const target = document.getElementById("points-result");

    if (target) {
        target.textContent = "Cargando...";
    }

    try {
        const data = await obtenerDatos("/web-api/points");
        if (target) {
            target.textContent = JSON.stringify(data, null, 2);
        }
    } catch (error) {
        if (target) {
            target.textContent = error.message;
        }
    }
}

async function guardarDigitalTwin() {
    const target = document.getElementById("save-result");

    if (target) {
        target.textContent = "Guardando...";
    }

    try {
        const data = await enviarPost("/web-api/save");
        if (target) {
            target.textContent = JSON.stringify(data, null, 2);
        }
    } catch (error) {
        if (target) {
            target.textContent = error.message;
        }
    }
}

async function cargarDigitalTwin(){
    const target = document.getElementById("load-result");

    if (target) {
        target.textContent = "Cargando el modelo...";
    }

    try {
        const data = await enviarPost("/web/api/load");
        if (target) {
            target.textContent = JSON.stringify(data, null, 2);
        }
    } catch (error) {
        if (target) {
            target.textContent = error.message;
        }
    }
}
async function importarSantraLegacy() {
    const textarea = document.getElementById("santra-json-input");
    const result = document.getElementById("santra-import-result");

    if (!textarea || !result) {
        return;
    }

    const rawText = textarea.value.trim();

    if (!rawText) {
        result.textContent = "Introduce primero el JSON de Santra Legacy.";
        return;
    }

    let parsed;
    try {
        parsed = JSON.parse(rawText);
    } catch (error) {
        result.textContent = "El texto no es un JSON válido: " + error.message;
        return;
    }

    result.textContent = "Enviando datos...";

    try {
        const data = await enviarPost("/web-api/import-santra-json", parsed);
        result.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        result.textContent = "Error al importar: " + error.message;
    }
}
document.getElementById("btn-santra-import")?.addEventListener("click", importarSantraLegacy);
document.getElementById("btn-health")?.addEventListener("click", cargarHealth);
document.getElementById("btn-version")?.addEventListener("click", cargarVersion);
document.getElementById("btn-devices")?.addEventListener("click", cargarDevices);
document.getElementById("btn-points")?.addEventListener("click", cargarPoints);
document.getElementById("btn-save")?.addEventListener("click", guardarDigitalTwin);
document.getElementById("btn-load")?.addEventListener("click", cargarDigitalTwin);