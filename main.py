def main():
    
    hikes = []

    def log_hike():
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
        print("Hike logged!")

    def view_hikes():
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

    while True:
        print("\nHIKING TRACKER")
        print("1. Log a hike")
        print("2. View hikes")
        print("3. View statistics")
        print("4. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            log_hike()
        elif choice == "2":
            view_hikes()
        elif choice == "4":
            print("Goodbye!")
            break   


if __name__ == "__main__":
    main()