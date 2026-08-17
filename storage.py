import json
import os

DATA_FILE = "hikes.json"
TEMP_FILE = "hikes.tmp"


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
        print("Warning: hikes.json contains invalid data.")
        return []