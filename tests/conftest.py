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


@pytest.fixture
def sample_gpx_file(tmp_path):
    gpx_content = """<?xml version="1.0"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1" version="1.1" creator="Test">
  <metadata>
    <name>Test Hike</name>
  </metadata>
  <trk>
    <trkseg>
      <trkpt lat="33.0000" lon="-117.0000">
        <ele>100.0</ele>
        <time>2026-08-17T15:00:00Z</time>
      </trkpt>
      <trkpt lat="33.0010" lon="-117.0010">
        <ele>110.0</ele>
        <time>2026-08-17T16:30:00Z</time>
      </trkpt>
    </trkseg>
  </trk>
</gpx>
"""

    filepath = tmp_path / "test_hike.gpx"
    filepath.write_text(gpx_content)

    return filepath