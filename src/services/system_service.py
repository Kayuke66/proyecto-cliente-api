import subprocess
import tomllib
from pathlib import Path


def get_git_revision_hash():
    try:
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
    except Exception:
        return "local-build"


def get_version():
    pyproject_path = Path(__file__).resolve().parent.parent.parent / "pyproject.toml"

    try:
        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)
            version = data["project"]["version"]
    except Exception:
        version = "0.0.0-error"

    return {
        "name": "Santra Edge Agent Backend",
        "version": version,
        "build": get_git_revision_hash()
    }