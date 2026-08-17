import json
from datetime import datetime
from storage import load_hikes, save_hikes
from hikes import log_hike, view_hikes,view_hike_details, delete_hike, edit_hike
from hike_statistics import view_statistics, view_monthly_statistics

   
# Main Program Loop
def main():
    hikes = load_hikes()

    while True:
        print("\nHIKING TRACKER")
        print("1. Log a hike")
        print("2. View hikes")
        print("3. View hike details")
        print("4. View all-time statistics")
        print("5. View monthly statistics")
        print("6. Edit a hike")
        print("7. Delete a hike")
        print("8. Exit")    

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
            view_monthly_statistics(hikes)
        elif choice == "6":
            edit_hike(hikes)
        elif choice == "7":     
            delete_hike(hikes)
        elif choice == "8":     
            print("Goodbye!")
            break   


if __name__ == "__main__":
    main()