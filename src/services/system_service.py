import os


def get_version():
    return {
        "name": os.getenv("SERVICE_NAME", "Santra™ Edge Agent Backend"),
        "version": os.getenv("VERSION", "1.0.0"),
        "build": os.getenv("BUILD", "0"),
    }