from tabulate import tabulate



def main_menu(db_manager):

    while True:
        print("\n--- Fire Incidents Database Menu ---")
        print("1. Display Fire Incidents from Porto")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            records = db_manager.fires_from_Porto()
            db_manager.display_records(records)
        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
