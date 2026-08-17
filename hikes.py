# Imports
from input_utils import (
    get_float, 
    get_int, 
    get_optional_float, 
    get_optional_int, 
    get_date, 
    get_optional_date, 
    get_time, 
    get_optional_time, 
    format_time
)

from storage import (
    save_hikes
)   

from hike_statistics import (
    calculate_pace,
    format_pace,
    calculate_elevation_per_mile
)

# Hiking Functions
def log_hike(hikes):
    date = get_date("Date (YYYY-MM-DD): ")
    trail = input("Trail name: ")
    distance = get_float("Distance (miles): ", minimum=0)
    elevation_gain = get_int("Elevation gain (feet): ", minimum=0)
    total_time = get_time("Total time (HH:MM): ")
    pack_weight = get_float("Pack weight (lbs): ", minimum=0)

    hike = {
        "date": date,
        "trail": trail,
        "distance": distance,
        "elevation_gain": elevation_gain,
        "total_time": total_time,
        "pack_weight": pack_weight,
    }

    hikes.append(hike)
    save_hikes(hikes)

    print("Hike logged!")

def view_hikes(hikes):
    if not hikes:
        print("No hikes logged yet.")
        return
    
    print("\nHIKING LOG")
    
    for index, hike in enumerate(hikes, start=1):
        pace = calculate_pace(hike["total_time"], hike["distance"])
        print(
            f"{index}. {hike['trail']} - {hike['date']} - {hike['distance']:.2f} miles - {format_pace(pace)} / mile"
        )

def view_hike_details(hikes):
    if not hikes:
        print("No hikes logged yet.")
        return
    
    view_hikes(hikes)
    index = get_int("Enter the number of the hike to edit: ",minimum=1) - 1

    if 0 <= index < len(hikes):
        hike = hikes[index]
        pace = calculate_pace(hike["total_time"], hike["distance"])
        elevation_per_mile = calculate_elevation_per_mile(hike["elevation_gain"], hike["distance"])
        print(f"\nDetails for {hike['trail']} - {hike['date']}:")
        print(f"Distance: {hike['distance']:.2f} miles")
        print(f"Elevation Gain: {hike['elevation_gain']} feet")
        print(f"Elevation per Mile: {elevation_per_mile:.0f} feet/mile")
        print(f"Total Time: {format_time(hike['total_time'])}")
        print(f"Pace: {format_pace(pace)} / mile")
       
        print(f"Pack Weight: {hike['pack_weight']} lbs")
    else:
        print("Invalid hike number.")

def delete_hike(hikes):
    if not hikes:
        print("No hikes logged yet.")
        return
    
    view_hikes(hikes)
    index = get_int("Enter the number of the hike to edit: ",minimum=1) - 1

    if 0 <= index < len(hikes):
        deleted_hike = hikes.pop(index)
        save_hikes(hikes)
        print(f"Deleted hike: {deleted_hike['trail']} - {deleted_hike['date']}")
    else:
        print("Invalid hike number.")


def edit_hike(hikes):
    if not hikes:
        print("No hikes logged yet.")
        return
    
    view_hikes(hikes)
    index = get_int("Enter the number of the hike to edit: ",minimum=1) - 1

    if 0 <= index < len(hikes):
        hike = hikes[index]
        print(f"Editing hike: {hike['trail']} - {hike['date']}")

        date = get_optional_date(f"Date ({hike['date']}): ", hike['date'])
        trail = input(f"Trail name ({hike['trail']}): ") or hike['trail']
        distance = get_optional_float(f"Distance (miles) ({hike['distance']}): ", hike['distance'], minimum=0)
        elevation_gain = get_optional_int(f"Elevation gain (feet) ({hike['elevation_gain']}): ", hike['elevation_gain'], minimum=0)
        total_time = get_optional_time(f"Total time (HH:MM) ({format_time(hike['total_time'])}): ", hike["total_time"])       
        pack_weight = get_optional_float(f"Pack weight (lbs) ({hike['pack_weight']}): ", hike['pack_weight'], minimum=0)

        hike.update({
            "date": date,
            "trail": trail,
            "distance": distance,
            "elevation_gain": elevation_gain,
            "total_time": total_time,
            "pack_weight": pack_weight,
        })

        save_hikes(hikes)
        print("Hike updated!")
    else:
        print("Invalid hike number.")