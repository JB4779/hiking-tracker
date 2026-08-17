from hike_statistics import (
    calculate_pace,
    format_pace,
    calculate_elevation_per_mile,
    get_hikes_for_month,
    get_hikes_for_year,
    calculate_statistics,
)


test_hikes = [
    {
        "date": "2026-08-10",
        "trail": "Trail A",
        "distance": 5.0,
        "elevation_gain": 500,
        "total_time": 120,
        "pack_weight": 10.0,
    },
    {
        "date": "2026-08-15",
        "trail": "Trail B",
        "distance": 8.0,
        "elevation_gain": 1000,
        "total_time": 180,
        "pack_weight": 12.0,
    },
    {
        "date": "2025-07-20",
        "trail": "Trail C",
        "distance": 3.0,
        "elevation_gain": 300,
        "total_time": 75,
        "pack_weight": 8.0,
    },
]

def test_calculate_pace():
    assert calculate_pace(60, 3) == 20


def test_calculate_pace_zero_distance():
    assert calculate_pace(60, 0) == 0


def test_format_pace():
    assert format_pace(29.15) == "29:09"


def test_elevation_per_mile():
    assert calculate_elevation_per_mile(1000, 5) == 200


def test_get_hikes_for_month():
    result = get_hikes_for_month(test_hikes, 2026, 8)

    assert len(result) == 2
    assert result[0]["trail"] == "Trail A"
    assert result[1]["trail"] == "Trail B"


def test_get_hikes_for_year():
    result = get_hikes_for_year(test_hikes, 2026)

    assert len(result) == 2
    assert result[0]["trail"] == "Trail A"
    assert result[1]["trail"] == "Trail B"


def test_calculate_statistics():
    stats = calculate_statistics(test_hikes)

    assert stats["total_hikes"] == 3
    assert stats["total_distance"] == 16.0
    assert stats["total_elevation_gain"] == 1800
    assert stats["total_time"] == 375
    assert stats["average_distance"] == 16.0 / 3
    assert stats["longest_hike"]["trail"] == "Trail B"
    assert stats["shortest_hike"]["trail"] == "Trail C"


def test_calculate_statistics_empty():
    assert calculate_statistics([]) is None