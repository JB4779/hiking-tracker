import json
from datetime import datetime
from storage import load_hikes, save_hikes
from hikes import log_hike, view_hikes, delete_hike, edit_hike
from statistics import view_statistics

   
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