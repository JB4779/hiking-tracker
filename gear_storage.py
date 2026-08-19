import json

GEAR_FILE = "gear.json"


def save_gear(gear):
    with open(GEAR_FILE, "w") as file:
        json.dump(gear, file, indent=4)


def load_gear():
    try:
        with open(GEAR_FILE, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        return []