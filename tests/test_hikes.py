import hikes
from hikes import (
    view_hikes,
    view_hike_details,
    delete_hike,
    edit_hike,
    log_hike,
)

def test_view_hikes(sample_hikes, capsys):
    hikes.view_hikes(sample_hikes)

    captured = capsys.readouterr()

    assert "Trail A" in captured.out
    assert "Trail B" in captured.out
    assert "Trail C" in captured.out
    assert "24:00 / mile" in captured.out


def test_view_hikes_empty(capsys):
    hikes.view_hikes([])

    captured = capsys.readouterr()

    assert "No hikes logged yet." in captured.out


def test_delete_hike(sample_hikes, monkeypatch, capsys):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: "2"
    )

    monkeypatch.setattr(
        hikes,
        "save_hikes",
        lambda hikes: None
    )

    hikes.delete_hike(sample_hikes)

    captured = capsys.readouterr()

    assert len(sample_hikes) == 2
    assert sample_hikes[0]["trail"] == "Trail A"
    assert sample_hikes[1]["trail"] == "Trail C"
    assert "Deleted hike: Trail B" in captured.out


def test_delete_hike_invalid_number(sample_hikes, monkeypatch, capsys):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: "99"
    )

    monkeypatch.setattr(
        hikes,
        "save_hikes",
        lambda hikes: None
    )

    hikes.delete_hike(sample_hikes)

    captured = capsys.readouterr()

    assert len(sample_hikes) == 3
    assert "Invalid hike number." in captured.out


def test_delete_hike_empty(capsys):
    hikes.delete_hike([])

    captured = capsys.readouterr()

    assert "No hikes logged yet." in captured.out


def test_view_hike_details(sample_hikes, monkeypatch, capsys):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: "1"
    )

    hikes.view_hike_details(sample_hikes)

    captured = capsys.readouterr()

    assert "Trail A" in captured.out
    assert "5.00 miles" in captured.out
    assert "500 feet" in captured.out
    assert "100 feet/mile" in captured.out
    assert "02:00" in captured.out
    assert "24:00 / mile" in captured.out
    assert "10.0 lbs" in captured.out


def test_view_hike_details_invalid_number(sample_hikes, monkeypatch, capsys):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: "99"
    )

    hikes.view_hike_details(sample_hikes)

    captured = capsys.readouterr()

    assert "Invalid hike number." in captured.out


def test_view_hike_details_empty(capsys):
    hikes.view_hike_details([])

    captured = capsys.readouterr()

    assert "No hikes logged yet." in captured.out


def test_edit_hike_changes_trail_name(sample_hikes, monkeypatch, capsys):
    responses = iter([
        "1",          # select Trail A
        "",           # keep date
        "New Trail",  # change trail name
        "",           # keep distance
        "",           # keep elevation
        "",           # keep total time
        "",           # keep pack weight
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    monkeypatch.setattr(
        hikes,
        "save_hikes",
        lambda hikes: None
    )

    hikes.edit_hike(sample_hikes)

    captured = capsys.readouterr()

    assert sample_hikes[0]["trail"] == "New Trail"
    assert sample_hikes[0]["date"] == "2026-08-10"
    assert sample_hikes[0]["distance"] == 5.0
    assert sample_hikes[0]["elevation_gain"] == 500
    assert sample_hikes[0]["total_time"] == 120
    assert sample_hikes[0]["pack_weight"] == 10.0

    assert "Hike updated!" in captured.out


def test_edit_hike_changes_all_fields(sample_hikes, monkeypatch):
    responses = iter([
        "1",            # select Trail A
        "2026-09-01",   # new date
        "Updated Trail",
        "6.5",          # distance
        "700",          # elevation
        "2:30",         # total time
        "15.5",         # pack weight
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    monkeypatch.setattr(
        hikes,
        "save_hikes",
        lambda hikes: None
    )

    hikes.edit_hike(sample_hikes)

    edited = sample_hikes[0]

    assert edited["date"] == "2026-09-01"
    assert edited["trail"] == "Updated Trail"
    assert edited["distance"] == 6.5
    assert edited["elevation_gain"] == 700
    assert edited["total_time"] == 150
    assert edited["pack_weight"] == 15.5


def test_edit_hike_invalid_number(sample_hikes, monkeypatch, capsys):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: "99"
    )

    monkeypatch.setattr(
        hikes,
        "save_hikes",
        lambda hikes: None
    )

    hikes.edit_hike(sample_hikes)

    captured = capsys.readouterr()

    assert len(sample_hikes) == 3
    assert "Invalid hike number." in captured.out


def test_edit_hike_empty(capsys):
    hikes.edit_hike([])

    captured = capsys.readouterr()

    assert "No hikes logged yet." in captured.out


def test_log_hike_adds_hike(sample_hikes, monkeypatch, capsys):
    responses = iter([
        "2026-09-10",   # date
        "New Trail",    # trail
        "6.5",          # distance
        "800",          # elevation gain
        "2:15",         # total time
        "14.0",         # pack weight
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    monkeypatch.setattr(
        hikes,
        "save_hikes",
        lambda hikes: None
    )

    hikes.log_hike(sample_hikes)

    captured = capsys.readouterr()

    assert len(sample_hikes) == 4

    new_hike = sample_hikes[-1]

    assert new_hike["date"] == "2026-09-10"
    assert new_hike["trail"] == "New Trail"
    assert new_hike["distance"] == 6.5
    assert new_hike["elevation_gain"] == 800
    assert new_hike["total_time"] == 135
    assert new_hike["pack_weight"] == 14.0

    assert "Hike logged!" in captured.out


def test_log_hike_calls_save(sample_hikes, monkeypatch):
    responses = iter([
        "2026-09-10",
        "New Trail",
        "6.5",
        "800",
        "2:15",
        "14.0",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    save_called = {"value": False}

    def fake_save(hikes_to_save):
        save_called["value"] = True

    monkeypatch.setattr(
        hikes,
        "save_hikes",
        fake_save
    )

    hikes.log_hike(sample_hikes)

    assert save_called["value"] is True


def test_view_hike_details_with_moving_time(monkeypatch, capsys):
    hikes = [
        {
            "date": "2026-06-13",
            "trail": "NIX Nature Center - North Loop",
            "distance": 4.73,
            "elevation_gain": 680,
            "total_time": 122,
            "recorded_time": 122,
            "moving_time": 105,
            "stopped_time": 17,
            "recording_gap_time": 0,
            "pack_weight": None,
        }
    ]

    monkeypatch.setattr("builtins.input", lambda _: "1")

    view_hike_details(hikes)

    output = capsys.readouterr().out

    assert "Total Time: 02:02" in output
    assert "Recorded Time: 02:02" in output
    assert "Moving Time: 01:45" in output
    assert "Stopped Time: 00:17" in output
    assert "Recording Gap: 00:00" in output
    assert "Elapsed Pace: 25:48 / mile" in output
    assert "Moving Pace: 22:12 / mile" in output
    