import pytest


@pytest.fixture
def sample_hikes():
    return [
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