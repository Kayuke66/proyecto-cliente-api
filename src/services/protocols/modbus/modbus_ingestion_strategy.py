class ModbusIngestionStrategy:
    def import_device(self, device: dict, context: dict, twin_service) -> None:
        for bloque in device.get("bloques", []):
            for p in bloque.get("puntos", []):
                hierarchy = context["buildHierarchy"](
                    p.get("area"),
                    "NOT_ASSIGNED",
                )

                twin_service.create_point(
                    {
                        "id": f'{device["device_id"]}:modbus:{p.get("add")}',
                        "name": p.get("desc") or "",
                        "description": p.get("desc") or "",
                        "deviceId": str(device["device_id"]),
                        "metric": context["normalizeMetric"](p.get("desc") or ""),
                        "objectType": "modbus",
                        "objectInstance": p.get("add") or "",
                        "type": "digital" if p.get("digital") else "analog",
                        "writable": bool(p.get("write")),
                        "unit": p.get("unidad") or "",
                        "scale": p.get("escala") if p.get("escala") is not None else 1,
                        "offset": p.get("desplazamiento") if p.get("desplazamiento") is not None else 0,
                        "source": "physical",
                        "metadata": {
                            "protocol": "modbus",
                            "address": p.get("add"),
                            "operationCode": bloque.get("operation_code"),
                            "wordSize": bloque.get("wordSize"),
                        },
                    },
                    hierarchy,
                )