from calendar import month_name

from input_utils import format_time, get_int
from datetime import datetime


def view_statistics(hikes):
    if not hikes:
        print("No hikes logged yet.")
        return
    
    total_distance = sum(hike['distance'] for hike in hikes)
    total_elevation_gain = sum(hike['elevation_gain'] for hike in hikes)
    total_time = sum(hike['total_time'] for hike in hikes)
    average_distance = total_distance / len(hikes)
    average_pace = calculate_pace(total_time, total_distance)
    average_elevation_gain = total_elevation_gain / len(hikes)
    average_time = total_time / len(hikes)
    longest_hike = max(hikes, key=lambda hike: hike["distance"])
    shortest_hike = min(hikes, key=lambda hike: hike["distance"])

    print(f"Total Hikes: {len(hikes)}")
    print(f"Total Distance: {total_distance:.2f} miles")
    print(f"Total Elevation Gain: {total_elevation_gain} feet")
    print(f"Total Time: {format_time(total_time)}")
    print(f"Average Distance: {average_distance:.2f} miles")
    print(f"Average Pace: {format_pace(average_pace)} / mile")
    print(f"Average Elevation Gain: {average_elevation_gain:.2f} feet")
    print(f"Average Time: {average_time:.2f} minutes")
    print(f"Longest Hike: {longest_hike['trail']} - {longest_hike['distance']:.2f} miles")
    print(f"Shortest Hike: {shortest_hike['trail']} - {shortest_hike['distance']:.2f} miles")

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
    
    total_distance = sum(hike['distance'] for hike in monthly_hikes)
    total_elevation_gain = sum(hike['elevation_gain'] for hike in monthly_hikes)
    total_time = sum(hike['total_time'] for hike in monthly_hikes)
    longest_hike = max(monthly_hikes, key=lambda hike: hike["distance"])
    shortest_hike = min(monthly_hikes, key=lambda hike: hike["distance"])
    average_distance = total_distance / len(monthly_hikes)
 

    print(f"\n{month_name.upper()} {year} STATISTICS")
    print(f"Total Hikes: {len(monthly_hikes)}")
    print(f"Total Distance: {total_distance:.2f} miles")
    print(f"Total Elevation Gain: {total_elevation_gain} feet")
    print(f"Total Time: {format_time(total_time)}")
    print(f"Average Distance: {average_distance:.2f} miles")
    print(f"Average Pace: {format_pace(calculate_pace(total_time, total_distance))} / mile")
    print(f"Longest Hike: {longest_hike['trail']} - {longest_hike['distance']:.2f} miles")
    print(f"Shortest Hike: {shortest_hike['trail']} - {shortest_hike['distance']:.2f} miles")

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