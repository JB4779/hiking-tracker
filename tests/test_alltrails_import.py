import alltrails_import
from alltrails_import import (
    haversine_distance,
    smooth_elevations,
    calculate_elevation_change,
    parse_gpx_file,
    get_activity_name,
    get_track_points,
    get_track_times,
    get_activity_date,
    calculate_total_time,
    convert_gpx_to_hike,
    is_duplicate_hike,
)


def test_haversine_same_point():
    distance = haversine_distance(
        33.60807,
        -117.76362,
        33.60807,
        -117.76362,
    )

    assert distance == 0


def test_smooth_elevations():
    elevations = [100, 110, 120]

    result = smooth_elevations(
        elevations,
        window_size=1,
    )

    assert result == [
        105.0,
        110.0,
        115.0,
    ]    


def test_calculate_elevation_change():
    elevations = [
        100,
        110,
        105,
        120,
    ]

    gain, loss = calculate_elevation_change(elevations)

    assert round(gain) == 82
    assert round(loss) == 16   


def test_parse_gpx_file(sample_gpx_file):
    root = parse_gpx_file(sample_gpx_file)

    assert root is not None


def test_get_activity_name(sample_gpx_file):
    root = parse_gpx_file(sample_gpx_file)

    assert get_activity_name(root) == "Test Hike"


def test_get_track_points(sample_gpx_file):
    root = parse_gpx_file(sample_gpx_file)
    points = get_track_points(root)

    assert len(points) == 2


def test_track_times(sample_gpx_file):
    root = parse_gpx_file(sample_gpx_file)
    points = get_track_points(root)

    start, end = get_track_times(points)

    assert get_activity_date(start) == "2026-08-17"
    assert calculate_total_time(start, end) == 90


def test_convert_gpx_to_hike(sample_gpx_file):
    hike = convert_gpx_to_hike(sample_gpx_file)

    assert hike["date"] == "2026-08-17"
    assert hike["trail"] == "Test Hike"
    assert hike["total_time"] == 90
    assert hike["moving_time"] is None
    assert hike["pack_weight"] is None
    assert hike["source"] == "alltrails"

    assert hike["distance"] > 0
    assert hike["elevation_gain"] == 0
    assert hike["elevation_loss"] == 0


def test_is_duplicate_hike_exact_match(sample_hikes):
    hike = sample_hikes[0].copy()

    assert is_duplicate_hike(hike, sample_hikes) is True


def test_is_duplicate_hike_new_hike(sample_hikes):
    hike = {
        "date": "2026-09-01",
        "trail": "New Trail",
        "distance": 7.5,
        "elevation_gain": 900,
        "total_time": 180,
        "moving_time": None,
        "pack_weight": None,
        "source": "alltrails",
    }

    assert is_duplicate_hike(hike, sample_hikes) is False


def test_is_duplicate_hike_different_distance(sample_hikes):
    hike = sample_hikes[0].copy()
    hike["distance"] = 5.1

    assert is_duplicate_hike(hike, sample_hikes) is False


def test_import_alltrails_hikes_no_files(
    sample_hikes,
    tmp_path,
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        alltrails_import,
        "IMPORT_FOLDER",
        tmp_path,
    )

    alltrails_import.import_alltrails_hikes(sample_hikes)

    captured = capsys.readouterr()

    assert "No AllTrails GPX files found." in captured.out
    assert len(sample_hikes) == 3


def test_import_alltrails_hikes_imports_new_hike(
    sample_hikes,
    tmp_path,
    monkeypatch,
    capsys,
):
    fake_gpx = tmp_path / "new_hike.gpx"
    fake_gpx.write_text("<gpx></gpx>")

    monkeypatch.setattr(
        alltrails_import,
        "IMPORT_FOLDER",
        tmp_path,
    )

    new_hike = {
        "date": "2026-09-01",
        "trail": "Imported Trail",
        "distance": 7.5,
        "elevation_gain": 900,
        "elevation_loss": 850,
        "total_time": 180,
        "moving_time": None,
        "pack_weight": None,
        "source": "alltrails",
    }

    monkeypatch.setattr(
        alltrails_import,
        "convert_gpx_to_hike",
        lambda filepath: new_hike,
    )

    save_called = {"value": False}

    def fake_save(hikes_to_save):
        save_called["value"] = True

    monkeypatch.setattr(
        alltrails_import,
        "save_hikes",
        fake_save,
    )

    alltrails_import.import_alltrails_hikes(sample_hikes)

    captured = capsys.readouterr()

    assert len(sample_hikes) == 4
    assert sample_hikes[-1] == new_hike
    assert save_called["value"] is True
    assert "Imported: Imported Trail - 2026-09-01 - 7.50 miles" in captured.out
    assert "Imported: 1" in captured.out
    assert "Skipped duplicates: 0" in captured.out


def test_import_alltrails_hikes_skips_duplicate(
    sample_hikes,
    tmp_path,
    monkeypatch,
    capsys,
):
    fake_gpx = tmp_path / "duplicate.gpx"
    fake_gpx.write_text("<gpx></gpx>")

    monkeypatch.setattr(
        alltrails_import,
        "IMPORT_FOLDER",
        tmp_path,
    )

    duplicate_hike = sample_hikes[0].copy()

    monkeypatch.setattr(
        alltrails_import,
        "convert_gpx_to_hike",
        lambda filepath: duplicate_hike,
    )

    save_called = {"value": False}

    def fake_save(hikes_to_save):
        save_called["value"] = True

    monkeypatch.setattr(
        alltrails_import,
        "save_hikes",
        fake_save,
    )

    alltrails_import.import_alltrails_hikes(sample_hikes)

    captured = capsys.readouterr()

    assert len(sample_hikes) == 3
    assert save_called["value"] is False
    assert "Skipped duplicate:" in captured.out
    assert "Imported: 0" in captured.out
    assert "Skipped duplicates: 1" in captured.out


def test_import_alltrails_hikes_mixed_batch(
    sample_hikes,
    tmp_path,
    monkeypatch,
    capsys,
):
    duplicate_file = tmp_path / "duplicate.gpx"
    new_file = tmp_path / "new.gpx"

    duplicate_file.write_text("<gpx></gpx>")
    new_file.write_text("<gpx></gpx>")

    monkeypatch.setattr(
        alltrails_import,
        "IMPORT_FOLDER",
        tmp_path,
    )

    duplicate_hike = sample_hikes[0].copy()

    new_hike = {
        "date": "2026-09-01",
        "trail": "Imported Trail",
        "distance": 7.5,
        "elevation_gain": 900,
        "elevation_loss": 850,
        "total_time": 180,
        "moving_time": None,
        "pack_weight": None,
        "source": "alltrails",
    }

    def fake_convert(filepath):
        if filepath.name == "duplicate.gpx":
            return duplicate_hike

        return new_hike

    monkeypatch.setattr(
        alltrails_import,
        "convert_gpx_to_hike",
        fake_convert,
    )

    save_called = {"value": False}

    def fake_save(hikes_to_save):
        save_called["value"] = True

    monkeypatch.setattr(
        alltrails_import,
        "save_hikes",
        fake_save,
    )

    alltrails_import.import_alltrails_hikes(sample_hikes)

    captured = capsys.readouterr()

    assert len(sample_hikes) == 4
    assert sample_hikes[-1] == new_hike
    assert save_called["value"] is True

    assert "Imported: 1" in captured.out
    assert "Skipped duplicates: 1" in captured.out
