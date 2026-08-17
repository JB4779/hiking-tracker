from calendar import month_name

from input_utils import format_time, get_int
from datetime import datetime


def view_statistics(hikes):
    if not hikes:
        print("No hikes logged yet.")
        return
    
    stats = calculate_statistics(hikes) 

    print(f"Total Hikes: {len(hikes)}")
    print(f"Total Distance: {stats['total_distance']:.2f} miles")
    print(f"Total Elevation Gain: {stats['total_elevation_gain']} feet")
    print(f"Total Time: {format_time(stats['total_time'])}")
    print(f"Average Distance: {stats['average_distance']:.2f} miles")
    print(f"Average Pace: {format_pace(stats['average_pace'])} / mile")
    print(f"Average Elevation Gain: {stats['average_elevation_gain']:.2f} feet")
    print(f"Average Time: {stats['average_time']:.2f} minutes")
    print(f"Longest Hike: {stats['longest_hike']['trail']} - {stats['longest_hike']['distance']:.2f} miles")
    print(f"Shortest Hike: {stats['shortest_hike']['trail']} - {stats['shortest_hike']['distance']:.2f} miles")


def view_monthly_statistics(hikes):
    year = get_int("Enter year (YYYY): ")
    month = get_int("Enter month (1-12): ")
    if month < 1 or month > 12:
        print("Invalid month. Please enter a number from 1 to 12.")
        return

    month_name = datetime(year, month, 1).strftime("%B")

    monthly_hikes = get_hikes_for_month(hikes, year, month)

    if not monthly_hikes:
        print(f"No hikes logged for {month_name}/{year}.")
        return
    
    stats = calculate_statistics(monthly_hikes)

    print(f"\n{month_name.upper()} {year} STATISTICS")
    print(f"Total Hikes: {len(monthly_hikes)}")
    print(f"Total Distance: {stats['total_distance']:.2f} miles")
    print(f"Total Elevation Gain: {stats['total_elevation_gain']} feet")
    print(f"Total Time: {format_time(stats['total_time'])}")
    print(f"Average Distance: {stats['average_distance']:.2f} miles")
    print(f"Average Pace: {format_pace(stats['average_pace'])} / mile")
    print(f"Longest Hike: {stats['longest_hike']['trail']} - {stats['longest_hike']['distance']:.2f} miles")
    print(f"Shortest Hike: {stats['shortest_hike']['trail']} - {stats['shortest_hike']['distance']:.2f} miles")


def calculate_statistics(hikes):
    total_distance = sum(hike["distance"] for hike in hikes)
    total_elevation_gain = sum(hike["elevation_gain"] for hike in hikes)
    total_time = sum(hike["total_time"] for hike in hikes)

    return {
        "total_hikes": len(hikes),
        "total_distance": total_distance,
        "total_elevation_gain": total_elevation_gain,
        "average_elevation_gain": total_elevation_gain / len(hikes) if hikes else 0,
        "total_time": total_time,
        "average_distance": total_distance / len(hikes),
        "average_time": total_time / len(hikes) if hikes else 0,
        "average_pace": calculate_pace(total_time, total_distance),
        "longest_hike": max(hikes, key=lambda hike: hike["distance"]),
        "shortest_hike": min(hikes, key=lambda hike: hike["distance"]),
    } 


def calculate_pace(total_time, distance):
    if distance == 0:
        return 0
    return total_time / distance


def format_pace(pace):
    if pace == 0:
        return "0:00"

    total_seconds = round(pace * 60)
    minutes, seconds = divmod(total_seconds, 60)

    return f"{minutes}:{seconds:02d}"


def calculate_elevation_per_mile(total_elevation_gain, total_distance):
    if total_distance == 0:
        return 0
    return total_elevation_gain / total_distance


def get_hikes_for_month(hikes, year, month):
    monthly_hikes = []

    for hike in hikes:
        hike_date = datetime.strptime(hike["date"], "%Y-%m-%d")
        if hike_date.year == year and hike_date.month == month:
            monthly_hikes.append(hike)

    return monthly_hikes