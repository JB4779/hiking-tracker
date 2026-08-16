import json

DATA_FILE = "hikes.json"


def save_hikes(hikes):
    with open(DATA_FILE, "w") as file:
        json.dump(hikes, file, indent=4)

def load_hikes():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Warning: hikes.json contains invalid data.")
        return []