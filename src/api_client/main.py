from api_client.health import get_health
from api_client.system import get_version
from api_client.digital_twin import (
    digital_twin_tree,
    get_devices,
    get_all_points,
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

    print("\nDigital Twin Tree:")
    print(tree_data)

    print("\nDevices:")
    print(devices_data)

    print("\nPoints:")
    print(points_data)


if __name__ == "__main__":
    main()