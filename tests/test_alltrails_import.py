from alltrails_import import (
    haversine_distance,
    smooth_elevations,
    calculate_elevation_change,
)
from alltrails_import import (
    parse_gpx_file,
    get_activity_name,
    get_track_points,
    get_track_times,
    get_activity_date,
    calculate_total_time,
    convert_gpx_to_hike,
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
