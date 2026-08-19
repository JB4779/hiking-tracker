import json
import os
from pathlib import Path
from config_loader import load_app_config

APP_CONFIG = load_app_config()

DATA_FILE = Path(APP_CONFIG["data_files"]["hikes"])
TEMP_FILE = DATA_FILE.with_suffix(".tmp")


def save_hikes(hikes):
    try:
        with open(TEMP_FILE, "w") as file:
            json.dump(hikes, file, indent=4)

        os.replace(TEMP_FILE, DATA_FILE)

    except Exception:
        if os.path.exists(TEMP_FILE):
            os.remove(TEMP_FILE)
        raise

def load_hikes():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Warning: {DATA_FILE} contains invalid data.")
        return []