import json
import pytest
import config_loader


def test_load_config(tmp_path, monkeypatch):
    config_folder = tmp_path / "config"
    config_folder.mkdir()

    config_file = config_folder / "test_config.json"

    config_file.write_text(
        json.dumps(
            {
                "name": "test",
                "value": 123,
            }
        )
    )

    monkeypatch.setattr(
        config_loader,
        "CONFIG_FOLDER",
        config_folder,
    )

    result = config_loader.load_config("test_config.json")

    assert result["name"] == "test"
    assert result["value"] == 123


def test_load_app_config():
    config = config_loader.load_app_config()

    assert config["app_name"] == "Hiking Tracker"
    assert config["units"]["distance"] == "miles"


def test_load_gear_config():
    config = config_loader.load_gear_config()

    assert "categories" in config
    assert "statuses" in config
    assert "scoring" in config
    assert "targets" in config

    assert "Water" in config["categories"]
    assert "Filter" in config["categories"]["Water"]

    assert "Active" in config["statuses"]


def test_load_config_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(
        config_loader,
        "CONFIG_FOLDER",
        tmp_path,
    )

    with pytest.raises(RuntimeError):
        config_loader.load_config("missing.json")


def test_load_config_invalid_json(tmp_path, monkeypatch):
    config_file = tmp_path / "bad.json"
    config_file.write_text("this is not json")

    monkeypatch.setattr(
        config_loader,
        "CONFIG_FOLDER",
        tmp_path,
    )

    with pytest.raises(RuntimeError):
        config_loader.load_config("bad.json")


def test_load_import_config():
    config = config_loader.load_import_config()

    assert "alltrails" in config

    alltrails = config["alltrails"]

    assert alltrails["enabled"] is True
    assert alltrails["moving_speed_threshold_mph"] == 0.5

    assert (
        alltrails["folders"]["pending"]
        == "imports/alltrails/pending"
    )

    assert (
        alltrails["folders"]["processed"]
        == "imports/alltrails/processed"
    )

    assert (
        alltrails["folders"]["failed"]
        == "imports/alltrails/failed"
    )