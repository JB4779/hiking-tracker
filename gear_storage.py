import os
import json
from pathlib import Path

from config_loader import load_app_config

APP_CONFIG = load_app_config()

GEAR_FILE = Path(APP_CONFIG["data_files"]["gear"])
TEMP_FILE = GEAR_FILE.with_suffix(".tmp")


def save_gear(gear):
    try:
        with open(TEMP_FILE, "w") as file:
            json.dump(gear, file, indent=4)

        os.replace(TEMP_FILE, GEAR_FILE)

    except Exception:
        if os.path.exists(TEMP_FILE):
            os.remove(TEMP_FILE)
        raise


def load_gear():
    try:
        with open(GEAR_FILE, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        return []