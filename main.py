import json
from datetime import datetime
from storage import load_hikes, save_hikes
from hikes import log_hike, view_hikes,view_hike_details, delete_hike, edit_hike
from hike_statistics import view_statistics

   
# Main Program Loop
def main():
    hikes = load_hikes()

    while True:
        print("\nHIKING TRACKER")
        print("1. Log a hike")
        print("2. View hikes")
        print("3. View hike details")
        print("4. View statistics")
        print("5. Edit a hike")
        print("6. Delete a hike")
        print("7. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            log_hike(hikes)
        elif choice == "2":
            view_hikes(hikes)
        elif choice == "3":
            view_hike_details(hikes)
        elif choice == "4":
            view_statistics(hikes)
        elif choice == "5":
            edit_hike(hikes)
        elif choice == "6":
            delete_hike(hikes)
        elif choice == "7":     
            print("Goodbye!")
            break   


if __name__ == "__main__":
    main()