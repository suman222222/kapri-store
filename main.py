# main.py
from utils import clear_screen, print_header
import billing
import inventory

def display_menu():
    """Displays the main menu options."""
    print("\n--- MAIN MENU ---")
    print("1. View Data")
    print("2. Add Data (Billing System)")
    print("3. Delete Data")
    print("4. Exit")

def main():
    """Main execution loop of the Kapri Store program."""
    while True:
        clear_screen() # Clears the screen before showing the menu again
        
        # Display welcome message
        print_header("WELCOME TO KAPRI STORE MANAGEMENT SYSTEM")
        
        display_menu()
        
        choice = input("Please enter the number of the option you want to choose (1-4): ").strip()

        if choice == '1':
            clear_screen()
            inventory.view_data() # Calls function from inventory.py

        elif choice == '2':
            clear_screen()
            billing.add_items()   # Calls function from billing.py

        elif choice == '3':
            clear_screen()
            inventory.delete_data() # Calls function from inventory.py

        elif choice == '4':
            clear_screen()
            print("Exiting the Kapri Store system. Have a great day!")
            break # Exits the main loop, ending the program

        else:
            print("\n[Error] Invalid input. Please enter a number between 1 and 4.")
            input("Press Enter to try again...")

if __name__ == "__main__":
    main()