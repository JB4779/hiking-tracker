import xml.etree.ElementTree as ET
import shutil
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2
from pathlib import Path
from storage import save_hikes

NAMESPACE = {"gpx": "http://www.topografix.com/GPX/1/1"}
IMPORT_FOLDER = Path("imports/alltrails")

PENDING_FOLDER = IMPORT_FOLDER / "pending"
PROCESSED_FOLDER = IMPORT_FOLDER / "processed"
FAILED_FOLDER = IMPORT_FOLDER / "failed"


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


def is_duplicate_hike(hike, hikes):
    for existing_hike in hikes:
        same_date = existing_hike["date"] == hike["date"]
        same_trail = existing_hike["trail"] == hike["trail"]
        same_distance = existing_hike["distance"] == hike["distance"]

        if same_date and same_trail and same_distance:
            return True

    return False


def import_alltrails_hikes(hikes):
    create_import_folders()

    gpx_files = list(PENDING_FOLDER.glob("*.gpx"))

    if not gpx_files:
        print("No AllTrails GPX files found.")
        return

    imported = 0
    skipped = 0
    failed = 0

    for filepath in gpx_files:
        try:
            hike = convert_gpx_to_hike(filepath)

            if is_duplicate_hike(hike, hikes):
                print(
                    f"Skipped duplicate: "
                    f"{hike['trail']} - {hike['date']}"
                )

                skipped += 1

                destination = PROCESSED_FOLDER / filepath.name
                shutil.move(filepath, destination)

                continue

            hikes.append(hike)
            imported += 1

            print(
                f"Imported: "
                f"{hike['trail']} - {hike['date']} - "
                f"{hike['distance']:.2f} miles"
            )

            destination = PROCESSED_FOLDER / filepath.name
            shutil.move(filepath, destination)

        except Exception as error:
            failed += 1

            destination = FAILED_FOLDER / filepath.name
            shutil.move(filepath, destination)

            print(
                f"Failed: {filepath.name} - {error}"
            )

    if imported > 0:
        save_hikes(hikes)

    print("\nIMPORT COMPLETE")
    print(f"Imported: {imported}")
    print(f"Skipped duplicates: {skipped}")
    print(f"Failed: {failed}")


def create_import_folders():
    PENDING_FOLDER.mkdir(parents=True, exist_ok=True)
    PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)
    FAILED_FOLDER.mkdir(parents=True, exist_ok=True)

