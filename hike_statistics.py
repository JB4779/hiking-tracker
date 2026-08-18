from input_utils import format_time, get_int
from datetime import datetime


def view_statistics(hikes):
    if not hikes:
        print("No hikes logged yet.")
        return
    
    stats = calculate_statistics(hikes) 
    print_statistics(stats, "ALL-TIME STATISTICS")


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
    print_statistics(stats, f"{month_name.upper()} {year} STATISTICS")


def view_yearly_statistics(hikes):
    year = get_int("Enter year (YYYY): ")

    yearly_hikes = get_hikes_for_year(hikes, year)

    if not yearly_hikes:
        print(f"No hikes logged for {year}.")
        return
    
    stats = calculate_statistics(yearly_hikes)
    print_statistics(stats, f"{year} STATISTICS")


def calculate_statistics(hikes):
    if not hikes:
        return None
    
    total_distance = sum(hike["distance"] for hike in hikes)
    total_elevation_gain = sum(hike["elevation_gain"] for hike in hikes)
    total_time = sum(hike["total_time"] for hike in hikes)

    hikes_with_moving_time = [
        hike for hike in hikes
        if hike.get("moving_time") is not None
    ]

    total_moving_time = sum(
        hike["moving_time"]
        for hike in hikes_with_moving_time
    )

    moving_distance = sum(
        hike["distance"]
        for hike in hikes_with_moving_time
    )

    return {
        "total_hikes": len(hikes),
        "total_distance": total_distance,
        "total_elevation_gain": total_elevation_gain,
        "average_elevation_gain": total_elevation_gain / len(hikes),
        "total_time": total_time,
        "total_moving_time": total_moving_time,
        "moving_hike_count": len(hikes_with_moving_time),
        "average_distance": total_distance / len(hikes),
        "average_time": total_time / len(hikes),
        "average_pace": calculate_pace(total_time, total_distance),
        "average_moving_pace": calculate_pace(
            total_moving_time,
            moving_distance,
        ),
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


def get_hikes_for_year(hikes, year):
    yearly_hikes = []

    for hike in hikes:
        hike_date = datetime.strptime(hike["date"], "%Y-%m-%d")
        if hike_date.year == year:
            yearly_hikes.append(hike)

    return yearly_hikes

def print_statistics(stats, title):
    print(f"\n{title}")
    print(f"Total Hikes: {stats['total_hikes']}")
    print(f"Total Distance: {stats['total_distance']:.2f} miles")
    print(f"Total Elevation Gain: {stats['total_elevation_gain']} feet")
    print(f"Total Time: {format_time(stats['total_time'])}")
    print(f"Average Distance: {stats['average_distance']:.2f} miles")
    print(f"Average Elapsed Pace: {format_pace(stats['average_pace'])} / mile")
    if stats["moving_hike_count"] > 0:
        print(
            f"Average Moving Pace: "
            f"{format_pace(stats['average_moving_pace'])} / mile"
        )
    print(
        f"Longest Hike: {stats['longest_hike']['trail']} - "
        f"{stats['longest_hike']['distance']:.2f} miles"
    )
    print(
        f"Shortest Hike: {stats['shortest_hike']['trail']} - "
        f"{stats['shortest_hike']['distance']:.2f} miles"
    )