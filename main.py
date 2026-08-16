import json

DATA_FILE = "hikes.json"

# Input Helper Functions
def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_optional_float(prompt, current_value):
    while True:
        user_input = input(prompt)
        if user_input == "":
            return current_value
        try:
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_optional_int(prompt, current_value):
    while True:
        user_input = input(prompt)
        if user_input == "":
            return current_value
        try:
            return int(user_input)
        except ValueError:
            print("Invalid input. Please enter an integer.")

 
# Data Functions 
def save_hikes(hikes):
    with open(DATA_FILE, "w") as file:
        json.dump(hikes, file, indent=4)

def load_hikes():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Hiking Functions
def log_hike(hikes):
    date = input("Date: ")
    trail = input("Trail name: ")
    distance = get_float("Distance (miles): ")
    elevation_gain = get_int("Elevation gain (feet): ")
    total_time = get_int("Total time (minutes): ")
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
        print(
            f"{index}. {hike['trail']} - {hike['date']} - {hike['distance']:.2f} miles"
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
        
        date = input(f"Date ({hike['date']}): ") or hike['date']
        trail = input(f"Trail name ({hike['trail']}): ") or hike['trail']
        distance = get_optional_float(f"Distance (miles) ({hike['distance']}): ", hike['distance'])
        elevation_gain = get_optional_int(f"Elevation gain (feet) ({hike['elevation_gain']}): ", hike['elevation_gain'])
        total_time = get_optional_int(f"Total time (minutes) ({hike['total_time']}): ", hike['total_time'])
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


def view_statistics(hikes):
    if not hikes:
        print("No hikes logged yet.")
        return
    
    total_distance = sum(hike['distance'] for hike in hikes)
    total_elevation_gain = sum(hike['elevation_gain'] for hike in hikes)
    total_time = sum(hike['total_time'] for hike in hikes)
    average_distance = total_distance / len(hikes)
    average_elevation_gain = total_elevation_gain / len(hikes)
    average_time = total_time / len(hikes)
    longest_hike = max(hikes, key=lambda hike: hike["distance"])
    shortest_hike = min(hikes, key=lambda hike: hike["distance"])

    print(f"Total Hikes: {len(hikes)}")
    print(f"Total Distance: {total_distance:.2f} miles")
    print(f"Total Elevation Gain: {total_elevation_gain} feet")
    print(f"Total Time: {total_time} minutes")
    print(f"Average Distance: {average_distance:.2f} miles")
    print(f"Average Elevation Gain: {average_elevation_gain:.2f} feet")
    print(f"Average Time: {average_time:.2f} minutes")
    print(f"Longest Hike: {longest_hike['trail']} - {longest_hike['distance']:.2f} miles")
    print(f"Shortest Hike: {shortest_hike['trail']} - {shortest_hike['distance']:.2f} miles")
    
# Main Program Loop
def main():
    hikes = load_hikes()

    while True:
        print("\nHIKING TRACKER")
        print("1. Log a hike")
        print("2. View hikes")
        print("3. View statistics")
        print("4. Edit a hike") 
        print("5. Delete a hike")
        print("6. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            log_hike(hikes)
        elif choice == "2":
            view_hikes(hikes)
        elif choice == "3":
            view_statistics(hikes)
        elif choice == "4":
            edit_hike(hikes)
        elif choice == "5":
            delete_hike(hikes)
        elif choice == "6":
            print("Goodbye!")
            break   


if __name__ == "__main__":
    main()