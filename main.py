# Imports
from storage import load_hikes

from hikes import (
    log_hike,
    view_hikes,
    view_hike_details,
    delete_hike,
    edit_hike,
)

from hike_statistics import (
    view_statistics,
    view_monthly_statistics,
    view_yearly_statistics,
)

from alltrails_import import import_alltrails_hikes

from gear import (
    add_gear,
    view_gear,
    view_gear_details,
    edit_gear,
    delete_gear,
)

from gear_storage import load_gear


def hikes_menu(hikes):
    while True:
        print("\nHIKES")
        print("1.  Log a hike")
        print("2.  View hikes")
        print("3.  View hike details")
        print("4.  Import AllTrails hikes")
        print("5.  Edit a hike")
        print("6.  Delete a hike")
        print("0.  Back")

        choice = input("\nChoose an option: ")

        if choice == "1":
            log_hike(hikes)
        elif choice == "2":
            view_hikes(hikes)
        elif choice == "3":
            view_hike_details(hikes)
        elif choice == "4":
            import_alltrails_hikes(hikes)
        elif choice == "5":
            edit_hike(hikes)
        elif choice == "6":
            delete_hike(hikes)
        elif choice == "0":
            break
        else:
            print("Invalid option. Please choose 0-6.")


def statistics_menu(hikes):
    while True:
        print("\nSTATISTICS")
        print("1.  View all-time statistics")
        print("2.  View monthly statistics")
        print("3.  View yearly statistics")
        print("0.  Back")

        choice = input("\nChoose an option: ")

        if choice == "1":
            view_statistics(hikes)
        elif choice == "2":
            view_monthly_statistics(hikes)
        elif choice == "3":
            view_yearly_statistics(hikes)
        elif choice == "0":
            break
        else:
            print("Invalid option. Please choose 0-3.")


def gear_menu(gear):
    while True:
        print("\nGEAR")
        print("1.  Add gear")
        print("2.  View gear")
        print("3.  View gear details")
        print("4.  Edit gear")
        print("0.  Back")

        choice = input("\nChoose an option: ")

        if choice == "1":
            add_gear(gear)
        elif choice == "2":
            view_gear(gear)
        elif choice == "3":
            view_gear_details(gear)
        elif choice == "4":
            edit_gear(gear)
        elif choice == "5":
            delete_gear(gear)
        elif choice == "0":
            break
        else:
            print("Invalid option. Please choose 0-5.")


# Main Program Loop
def main():
    hikes = load_hikes()
    gear = load_gear()

    while True:
        print("\nHIKING TRACKER")
        print("1.  Hikes")
        print("2.  Gear")
        print("3.  Statistics")
        print("0.  Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            hikes_menu(hikes)
        elif choice == "2":
            gear_menu(gear)
        elif choice == "3":
            statistics_menu(hikes)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 0-3.")


if __name__ == "__main__":
    main()