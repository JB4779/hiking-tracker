import xml.etree.ElementTree as ET
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2

NAMESPACE = {"gpx": "http://www.topografix.com/GPX/1/1"}


def parse_gpx_file(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()

    return root


def get_activity_name(root):
    name = root.find("gpx:metadata/gpx:name", NAMESPACE)
    return name.text if name is not None else None


def get_track_points(root):
    return root.findall(".//gpx:trkpt", NAMESPACE)


def get_track_times(track_points):
    first_time = track_points[0].find("gpx:time", NAMESPACE).text
    last_time = track_points[-1].find("gpx:time", NAMESPACE).text

    start = datetime.fromisoformat(first_time.replace("Z", "+00:00"))
    end = datetime.fromisoformat(last_time.replace("Z", "+00:00"))

    return start, end


def get_activity_date(start_time):
    return start_time.date().isoformat()


def calculate_total_time(start_time, end_time):
    elapsed = end_time - start_time
    return round(elapsed.total_seconds() / 60)


def haversine_distance(lat1, lon1, lat2, lon2):
    earth_radius_miles = 3958.8

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius_miles * c


def calculate_distance(track_points):
    total_distance = 0

    for index in range(len(track_points) - 1):
        point1 = track_points[index]
        point2 = track_points[index + 1]

        lat1 = float(point1.attrib["lat"])
        lon1 = float(point1.attrib["lon"])
        lat2 = float(point2.attrib["lat"])
        lon2 = float(point2.attrib["lon"])

        total_distance += haversine_distance(
            lat1,
            lon1,
            lat2,
            lon2,
        )

    return total_distance


def get_elevations(track_points):
    elevations = []

    for point in track_points:
        elevation = point.find("gpx:ele", NAMESPACE)

        if elevation is not None:
            elevations.append(float(elevation.text))

    return elevations


def smooth_elevations(elevations, window_size=15):
    smoothed = []

    for index in range(len(elevations)):
        start = max(0, index - window_size)
        end = min(len(elevations), index + window_size + 1)

        window = elevations[start:end]

        smoothed.append(sum(window) / len(window))

    return smoothed


def calculate_elevation_change(elevations):
    total_gain = 0
    total_loss = 0

    for index in range(len(elevations) - 1):
        difference = elevations[index + 1] - elevations[index]

        if difference > 0:
            total_gain += difference
        elif difference < 0:
            total_loss += abs(difference)

    return total_gain * 3.28084, total_loss * 3.28084


def convert_gpx_to_hike(filepath):
    root = parse_gpx_file(filepath)

    track_points = get_track_points(root)
    start_time, end_time = get_track_times(track_points)

    distance = calculate_distance(track_points)

    elevations = get_elevations(track_points)
    smoothed_elevations = smooth_elevations(elevations)
    elevation_gain, elevation_loss = calculate_elevation_change(
        smoothed_elevations
    )

    hike = {
        "date": get_activity_date(start_time),
        "trail": get_activity_name(root),
        "distance": round(distance, 2),
        "elevation_gain": round(elevation_gain),
        "elevation_loss": round(elevation_loss),
        "total_time": calculate_total_time(start_time, end_time),
        "moving_time": None,
        "pack_weight": None,
        "source": "alltrails",
    }

    return hike


if __name__ == "__main__":
    filepath = "imports/alltrails/2026-06-13_nix_north_loop.gpx"

    hike = convert_gpx_to_hike(filepath)

    print(hike)



# if __name__ == "__main__":
#     root = parse_gpx_file(
#         "imports/alltrails/2026-06-13_nix_north_loop.gpx"
#     )

#     track_points = get_track_points(root)
#     start_time, end_time = get_track_times(track_points)
#     distance = calculate_distance(track_points)
#     elevations = get_elevations(track_points)

#     raw_gain, raw_loss = calculate_elevation_change(elevations)

#     print(get_activity_name(root))
#     print(f"Track points: {len(track_points)}")
#     print(f"Date: {get_activity_date(start_time)}")
#     print(f"Total time: {calculate_total_time(start_time, end_time)} minutes")
#     print(f"Distance: {distance:.2f} miles")
#     print(f"Raw elevation gain: {raw_gain:.0f} feet")
#     print(f"Raw elevation loss: {raw_loss:.0f} feet")

#     print("\nSmoothing comparison:")

#     for window_size in [3, 5, 10, 15, 20, 30]:
#         smoothed = smooth_elevations(
#             elevations,
#             window_size=window_size
#         )

#         gain, loss = calculate_elevation_change(smoothed)

#         print(
#             f"Window {window_size:>2}: "
#             f"Gain {gain:.0f} ft | "
#             f"Loss {loss:.0f} ft"
#         )