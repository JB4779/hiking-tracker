import json

DATA_FILE = "hikes.json"


def save_hikes(hikes):
    with open(DATA_FILE, "w") as file:
        json.dump(hikes, file, indent=4)

def load_hikes():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def log_hike(hikes):
    date = input("Date: ")
    trail = input("Trail name: ")
    distance = float(input("Distance (miles): "))
    elevation_gain = int(input("Elevation gain (feet): "))
    total_time = int(input("Total time (minutes): "))
    pack_weight = float(input("Pack weight (lbs): "))

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
    
    for hike in hikes:
        print(f"Date: {hike['date']}")
        print(f"Trail: {hike['trail']}")
        print(f"Distance: {hike['distance']} miles")
        print(f"Elevation Gain: {hike['elevation_gain']} feet")
        print(f"Total Time: {hike['total_time']} minutes")
        print(f"Pack Weight: {hike['pack_weight']} lbs")
        print()

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
    

def main():
    hikes = load_hikes()

    while True:
        print("\nHIKING TRACKER")
        print("1. Log a hike")
        print("2. View hikes")
        print("3. View statistics")
        print("4. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            log_hike(hikes)
        elif choice == "2":
            view_hikes(hikes)
        elif choice == "3":
            view_statistics(hikes)
        elif choice == "4":
            print("Goodbye!")
            break   


if __name__ == "__main__":
    main()