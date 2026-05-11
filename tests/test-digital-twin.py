import pytest

from api_client.digital_twin import (
    get_device_by_id,
    get_device_points,
    get_equipment_points,
    import_ede,
    import_santra_legacy_json,
    import_ede_from_file,
)

def test_error_device_by_id_si_no_hay_id():
    with pytest.raises(ValueError, match="El ID es obligatorio"):
        get_device_by_id("")

def test_error_device_points_si_no_hay_id():
    with pytest.raises(ValueError, match="El ID es obligatorio"):
        get_device_points("")

def test_error_equipment_points_si_no_hay_id():
    with pytest.raises(ValueError, match="El ID es obligatorio"):
        get_equipment_points("")

def test_error_import_sandra_legacy_json_si_no_hay_json():
    with pytest.raises(ValueError, match="Se requiere el archivo .json"):
        import_santra_legacy_json(None)

def test_error_import_santra_legacy_json_si_falta_id_planta():
    data = {
        "denominacion": "Test Site",
        "legalEntity": "B88888888",
        "language": "fr",
        "dispositivos": []
    }
    with pytest.raises(ValueError, match="No se ha introducido el siguiente campo: idPlanta"):
        import_santra_legacy_json(data)

def test_error_import_ede_si_no_hay_archivo_ede():
    with pytest.raises(ValueError, match="La petición requiere el archivo EDE."):
        import_ede(None)

def test_error_import_ede_si_no_hay_contenido():
    with pytest.raises(ValueError, match="La petición requiere el archivo EDE"):
        import_ede(None)

def test_error_import_ede_from_file_si_no_hay_ruta():
    with pytest.raises(ValueError, match="Se requiere la ruta del archivo EDE"):
        import_ede_from_file("")

def test_error_import_ede_from_file_si_no_existe():
    with pytest.raises(ValueError, match="No se encontró el archivo: archivo.ede"):
        import_ede_from_file("archivo.ede")