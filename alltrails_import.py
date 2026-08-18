import xml.etree.ElementTree as ET
import shutil
import re
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2
from pathlib import Path
from storage import save_hikes

NAMESPACE = {"gpx": "http://www.topografix.com/GPX/1/1"}
MOVING_SPEED_THRESHOLD = 0.5
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


def get_track_segments(root):
    return root.findall(".//gpx:trkseg", NAMESPACE)


def get_track_times(track_points):
    first_time = track_points[0].find("gpx:time", NAMESPACE).text
    last_time = track_points[-1].find("gpx:time", NAMESPACE).text

    start = datetime.fromisoformat(first_time.replace("Z", "+00:00"))
    end = datetime.fromisoformat(last_time.replace("Z", "+00:00"))

    return start, end


def get_activity_date(start_time):
    return start_time.date().isoformat()


def calculate_segment_distance(segment):
    track_points = segment.findall("gpx:trkpt", NAMESPACE)
    return calculate_distance(track_points)


def calculate_total_distance(segments):
    total_distance = 0

    for segment in segments:
        total_distance += calculate_segment_distance(segment)

    return total_distance


def calculate_total_time(start_time, end_time):
    elapsed = end_time - start_time
    return round(elapsed.total_seconds() / 60)


def get_segment_times(segment):
    track_points = segment.findall("gpx:trkpt", NAMESPACE)

    first_time = track_points[0].find("gpx:time", NAMESPACE).text
    last_time = track_points[-1].find("gpx:time", NAMESPACE).text

    start = datetime.fromisoformat(first_time.replace("Z", "+00:00"))
    end = datetime.fromisoformat(last_time.replace("Z", "+00:00"))

    return start, end


def calculate_recorded_time(segments):
    total_minutes = 0

    for segment in segments:
        start, end = get_segment_times(segment)
        total_minutes += (end - start).total_seconds() / 60

    return round(total_minutes)


def calculate_recording_gap_time(total_time, recorded_time):
    return total_time - recorded_time


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


def calculate_segment_moving_time(segment):
    track_points = segment.findall("gpx:trkpt", NAMESPACE)

    moving_seconds = 0
    stopped_seconds = 0

    for index in range(len(track_points) - 1):
        point1 = track_points[index]
        point2 = track_points[index + 1]

        lat1 = float(point1.attrib["lat"])
        lon1 = float(point1.attrib["lon"])
        lat2 = float(point2.attrib["lat"])
        lon2 = float(point2.attrib["lon"])

        time1_text = point1.find("gpx:time", NAMESPACE).text
        time2_text = point2.find("gpx:time", NAMESPACE).text

        time1 = datetime.fromisoformat(
            time1_text.replace("Z", "+00:00")
        )
        time2 = datetime.fromisoformat(
            time2_text.replace("Z", "+00:00")
        )

        elapsed_seconds = (time2 - time1).total_seconds()

        if elapsed_seconds <= 0:
            continue

        distance = haversine_distance(
            lat1,
            lon1,
            lat2,
            lon2,
        )

        elapsed_hours = elapsed_seconds / 3600

        speed = distance / elapsed_hours

        if speed >= MOVING_SPEED_THRESHOLD:
            moving_seconds += elapsed_seconds
        else:
            stopped_seconds += elapsed_seconds

    moving_minutes = round(moving_seconds / 60)
    stopped_minutes = round(stopped_seconds / 60)

    return moving_seconds, stopped_seconds


def calculate_total_moving_time(segments):
    total_moving_seconds = 0
    total_stopped_seconds = 0

    for segment in segments:
        moving_seconds, stopped_seconds = (
            calculate_segment_moving_time(segment)
        )

        total_moving_seconds += moving_seconds
        total_stopped_seconds += stopped_seconds

    moving_minutes = round(total_moving_seconds / 60)
    recorded_minutes = round(
        (total_moving_seconds + total_stopped_seconds) / 60
    )

    stopped_minutes = recorded_minutes - moving_minutes

    return moving_minutes, stopped_minutes


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


def calculate_segment_elevation_change(segment):
    track_points = segment.findall("gpx:trkpt", NAMESPACE)

    elevations = get_elevations(track_points)
    smoothed_elevations = smooth_elevations(elevations)

    return calculate_elevation_change(smoothed_elevations)


def calculate_total_elevation_change(segments):
    total_gain = 0
    total_loss = 0

    for segment in segments:
        gain, loss = calculate_segment_elevation_change(segment)

        total_gain += gain
        total_loss += loss

    return total_gain, total_loss


def convert_gpx_to_hike(filepath):
    root = parse_gpx_file(filepath)

    track_points = get_track_points(root)
    track_segments = get_track_segments(root)

    start_time, end_time = get_track_times(track_points)

    recorded_time = calculate_recorded_time(track_segments) 
    recording_gap_time = calculate_recording_gap_time(calculate_total_time(start_time, end_time), recorded_time,)   
    moving_time, stopped_time = calculate_total_moving_time(track_segments)

    distance = calculate_total_distance(track_segments)

    elevation_gain, elevation_loss = calculate_total_elevation_change(
    track_segments
)

    hike = {
        "date": get_activity_date(start_time),
        "trail": get_activity_name(root),
        "distance": round(distance, 2),
        "elevation_gain": round(elevation_gain),
        "elevation_loss": round(elevation_loss),
        "total_time": calculate_total_time(start_time, end_time),
        "recorded_time": recorded_time,
        "recording_gap_time": recording_gap_time,
        "moving_time": moving_time,
        "stopped_time": stopped_time,
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

                processed_filename = create_processed_filename(hike)
                destination = PROCESSED_FOLDER / processed_filename
                shutil.move(filepath, destination)

                continue

            hikes.append(hike)
            imported += 1

            print(
                f"Imported: "
                f"{hike['trail']} - {hike['date']} - "
                f"{hike['distance']:.2f} miles"
            )

            processed_filename = create_processed_filename(hike)
            destination = PROCESSED_FOLDER / processed_filename 
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


def create_processed_filename(hike):
    trail_name = hike["trail"].lower()

    # Remove apostrophes
    trail_name = trail_name.replace("'", "")

    # Replace other non-alphanumeric characters with dashes
    trail_name = re.sub(r"[^a-z0-9]+", "-", trail_name)

    # Remove leading/trailing dashes
    trail_name = trail_name.strip("-")

    return f"{hike['date']}_{trail_name}.gpx"

