import hike_statistics
from hike_statistics import (
    calculate_pace,
    format_pace,
    calculate_elevation_per_mile,
    get_hikes_for_month,
    get_hikes_for_year,
    calculate_statistics,
)


def test_calculate_pace():
    assert calculate_pace(60, 3) == 20


def test_calculate_pace_zero_distance():
    assert calculate_pace(60, 0) == 0


def test_format_pace():
    assert format_pace(29.15) == "29:09"


def test_elevation_per_mile():
    assert calculate_elevation_per_mile(1000, 5) == 200


def test_get_hikes_for_month(sample_hikes):
    result = get_hikes_for_month(sample_hikes, 2026, 8)

    assert len(result) == 2
    assert result[0]["trail"] == "Trail A"
    assert result[1]["trail"] == "Trail B"


def test_get_hikes_for_year(sample_hikes):
    result = get_hikes_for_year(sample_hikes, 2026)

    assert len(result) == 2
    assert result[0]["trail"] == "Trail A"
    assert result[1]["trail"] == "Trail B"


def test_calculate_statistics(sample_hikes):
    stats = calculate_statistics(sample_hikes)

    assert stats["total_hikes"] == 3
    assert stats["total_distance"] == 16.0
    assert stats["total_elevation_gain"] == 1800
    assert stats["total_time"] == 375
    assert stats["longest_hike"]["trail"] == "Trail B"
    assert stats["shortest_hike"]["trail"] == "Trail C"


def test_calculate_statistics_empty():
    assert calculate_statistics([]) is None


def test_view_statistics(sample_hikes, capsys):
    hike_statistics.view_statistics(sample_hikes)

    captured = capsys.readouterr()

    assert "ALL-TIME STATISTICS" in captured.out
    assert "Total Hikes: 3" in captured.out
    assert "Total Distance: 16.00 miles" in captured.out
    assert "Longest Hike: Trail B - 8.00 miles" in captured.out
    assert "Shortest Hike: Trail C - 3.00 miles" in captured.out


def test_view_statistics_empty(capsys):
    hike_statistics.view_statistics([])

    captured = capsys.readouterr()

    assert "No hikes logged yet." in captured.out


def test_view_monthly_statistics(sample_hikes, monkeypatch, capsys):
    responses = iter([
        "2026",  # year
        "8",     # month
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    hike_statistics.view_monthly_statistics(sample_hikes)

    captured = capsys.readouterr()

    assert "AUGUST 2026 STATISTICS" in captured.out
    assert "Total Hikes: 2" in captured.out
    assert "Total Distance: 13.00 miles" in captured.out
    assert "Longest Hike: Trail B - 8.00 miles" in captured.out
    assert "Shortest Hike: Trail A - 5.00 miles" in captured.out


def test_view_monthly_statistics_invalid_month(
    sample_hikes,
    monkeypatch,
    capsys,
):
    responses = iter([
        "2026",
        "13",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    hike_statistics.view_monthly_statistics(sample_hikes)

    captured = capsys.readouterr()

    assert "Invalid month. Please enter a number from 1 to 12." in captured.out


def test_view_monthly_statistics_no_hikes(
    sample_hikes,
    monkeypatch,
    capsys,
):
    responses = iter([
        "2026",
        "1",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    hike_statistics.view_monthly_statistics(sample_hikes)

    captured = capsys.readouterr()

    assert "No hikes logged for January/2026." in captured.out


def test_view_yearly_statistics(sample_hikes, monkeypatch, capsys):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: "2026"
    )

    hike_statistics.view_yearly_statistics(sample_hikes)

    captured = capsys.readouterr()

    assert "2026 STATISTICS" in captured.out
    assert "Total Hikes: 2" in captured.out
    assert "Total Distance: 13.00 miles" in captured.out
    assert "Longest Hike: Trail B - 8.00 miles" in captured.out
    assert "Shortest Hike: Trail A - 5.00 miles" in captured.out


def test_view_yearly_statistics_no_hikes(
    sample_hikes,
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: "2024"
    )

    hike_statistics.view_yearly_statistics(sample_hikes)

    captured = capsys.readouterr()

    assert "No hikes logged for 2024." in captured.out


def test_format_pace_zero():
    assert format_pace(0) == "0:00"


def test_elevation_per_mile_zero_distance():
    assert calculate_elevation_per_mile(1000, 0) == 0