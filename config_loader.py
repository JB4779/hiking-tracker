import json
from pathlib import Path


CONFIG_FOLDER = Path("config")


def load_config(filename):
    filepath = CONFIG_FOLDER / filename

    try:
        with open(filepath, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        raise RuntimeError(
            f"Configuration file not found: {filepath}"
        )

    except json.JSONDecodeError:
        raise RuntimeError(
            f"Invalid configuration file: {filepath}"
        )


def load_app_config():
    return load_config("app_config.json")


def load_gear_config():
    return load_config("gear_config.json")


def load_import_config():
    return load_config("import_config.json")