from api_client.health import get_health
from api_client.system import get_version
from api_client.digital_twin import (
    digital_twin_tree,
    get_devices,
    get_all_points,
    import_santra_legacy_json,
    save_digital_twin,
    load_digital_twin,
)


def main():
    health_data = get_health()
    version_data = get_version()
    tree_data = digital_twin_tree()
    devices_data = get_devices()
    points_data = get_all_points()

    print("Health:")
    print(health_data)

    print("\nVersion:")
    print(version_data)

    print("\nTree:")
    print(tree_data)

    print("\nDevices:")
    print(devices_data)

    print("\nPoints:")
    print(points_data)

    ejemplo_santra_legacy = {
        "idPlanta": "TESTSITE",
        "denominacion": "Test Site",
        "legalEntity": "B88888888",
        "language": "fr",
        "dispositivos": []
    }

    print("\nImport Santra Legacy JSON:")
    print(import_santra_legacy_json(ejemplo_santra_legacy))

    print("\nSave Digital Twin:")
    print(save_digital_twin())

    print("\nLoad Digital Twin:")
    print(load_digital_twin())

if __name__ == "__main__":
    main()