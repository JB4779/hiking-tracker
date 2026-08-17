#Imports
from storage import load_hikes
from hikes import (
    log_hike,
    view_hikes,
    view_hike_details,
    delete_hike,
    edit_hike
)
from hike_statistics import (
    view_statistics,
    view_monthly_statistics,
    view_yearly_statistics
)
   
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
        print("6. View yearly statistics")
        print("7. Edit a hike")
        print("8. Delete a hike")
        print("9. Exit")    

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
            view_yearly_statistics(hikes)
        elif choice == "7":
            edit_hike(hikes)
        elif choice == "8":     
            delete_hike(hikes)
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-9.") 


if __name__ == "__main__":
    main()