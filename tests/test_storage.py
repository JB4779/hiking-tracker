import pytest
import storage


def test_save_and_load_hikes(tmp_path):
    test_file = tmp_path / "hikes.json"
    temp_file = tmp_path / "hikes.tmp"

    storage.DATA_FILE = str(test_file)
    storage.TEMP_FILE = str(temp_file)

    hikes = [
        {
            "date": "2026-08-17",
            "trail": "Test Trail",
            "distance": 5.0,
            "elevation_gain": 500,
            "total_time": 120,
            "pack_weight": 10.0,
        }
    ]

    storage.save_hikes(hikes)

    loaded_hikes = storage.load_hikes()

    assert loaded_hikes == hikes


def test_load_hikes_file_not_found(tmp_path):
    test_file = tmp_path / "hikes.json"

    storage.DATA_FILE = str(test_file)

    result = storage.load_hikes()

    assert result == []


def test_load_hikes_invalid_json(tmp_path, capsys):
    test_file = tmp_path / "hikes.json"
    test_file.write_text("this is not valid json")

    storage.DATA_FILE = str(test_file)

    result = storage.load_hikes()
    captured = capsys.readouterr()

    assert result == []
    assert "contains invalid data." in captured.out
    assert "hikes.json" in captured.out


def test_failed_save_preserves_existing_file(tmp_path):
    test_file = tmp_path / "hikes.json"
    temp_file = tmp_path / "hikes.tmp"

    storage.DATA_FILE = str(test_file)
    storage.TEMP_FILE = str(temp_file)

    original_hikes = [
        {
            "date": "2026-08-17",
            "trail": "Good Hike",
            "distance": 5.0,
            "elevation_gain": 500,
            "total_time": 120,
            "pack_weight": 10.0,
        }
    ]

    storage.save_hikes(original_hikes)               # Good hike saved

    bad_hikes = [
        {
            "trail": "Bad Hike",
            "bad_value": {1, 2, 3},
        }
    ]

    with pytest.raises(TypeError):
        storage.save_hikes(bad_hikes)                # Bad hike attempted / JSON serialization fails

    loaded_hikes = storage.load_hikes()

    assert loaded_hikes == original_hikes            # Good hike still there
    assert not temp_file.exists()                    # Delete tmp file