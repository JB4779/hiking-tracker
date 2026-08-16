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
    load_hikes, 
    save_hikes
)   

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

from hike_statistics import (
    calculate_pace,
    format_pace
)

# Hiking Functions
def log_hike(hikes):
    date = get_date("Date (YYYY-MM-DD): ")
    trail = input("Trail name: ")
    distance = get_float("Distance (miles): ")
    elevation_gain = get_int("Elevation gain (feet): ")
    total_time = get_time("Total time (HH:MM): ")
    pack_weight = get_float("Pack weight (lbs): ")

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

def delete_hike(hikes):
    if not hikes:
        print("No hikes logged yet.")
        return
    
    view_hikes(hikes)
    index = get_int("Enter the number of the hike to delete: ") - 1

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
    index = get_int("Enter the number of the hike to edit: ") - 1

    if 0 <= index < len(hikes):
        hike = hikes[index]
        print(f"Editing hike: {hike['trail']} - {hike['date']}")

        date = get_optional_date(f"Date ({hike['date']}): ", hike['date'])
        trail = input(f"Trail name ({hike['trail']}): ") or hike['trail']
        distance = get_optional_float(f"Distance (miles) ({hike['distance']}): ", hike['distance'])
        elevation_gain = get_optional_int(f"Elevation gain (feet) ({hike['elevation_gain']}): ", hike['elevation_gain'])
        total_time = get_optional_time(f"Total time (HH:MM) ({format_time(hike['total_time'])}): ", hike["total_time"])       
        pack_weight = get_optional_float(f"Pack weight (lbs) ({hike['pack_weight']}): ", hike['pack_weight']    )

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