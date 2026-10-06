# main.py
from utils import clear_screen, print_header, pause
import billing
import inventory
import reports

def display_main_menu():
    print("\n---  KAPRI STORE MAIN MENU ---")
    print("1.  New Sale (Billing)")
    print("2.  Search Products")
    print("3.  View Transaction History")
    print("4.  Daily Sales Report")
    print("5.  Category Performance")
    print("6.   Low Stock Alerts")
    print("7.  Admin Panel")
    print("8.  Exit")

def display_admin_menu():
    print("\n--- 🔧 ADMIN PANEL ---")
    print("1. Restock Inventory")
    print("2. Delete All Transactions (DANGER)")
    print("3. Back to Main Menu")

def admin_panel():
    while True:
        clear_screen()
        print_header("ADMIN PANEL")
        display_admin_menu()
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '1':
            clear_screen()
            inventory.admin_restock()
        elif choice == '2':
            clear_screen()
            confirm = input("⚠️  Are you sure? Type 'DELETE' to confirm: ")
            if confirm == 'DELETE':
                from utils import save_json
                save_json('transactions.json', [])
                print("✔ All transactions deleted.")
            else:
                print("Cancelled.")
            pause()
        elif choice == '3':
            break
        else:
            print("Invalid choice.")
            pause()

def main():
    while True:
        clear_screen()
        print_header("WELCOME TO KAPRI STORE MANAGEMENT SYSTEM")
        display_main_menu()
        
        choice = input("\nPlease enter your choice (1-8): ").strip()

        if choice == '1':
            clear_screen()
            billing.add_items()
        elif choice == '2':
            clear_screen()
            inventory.search_products()
        elif choice == '3':
            clear_screen()
            inventory.view_data()
        elif choice == '4':
            clear_screen()
            reports.daily_sales_report()
        elif choice == '5':
            clear_screen()
            reports.category_performance()
        elif choice == '6':
            clear_screen()
            inventory.check_low_stock()
        elif choice == '7':
            admin_panel()
        elif choice == '8':
            clear_screen()
            print("=" * 45)
            print("   Thank you for using Kapri Store System!")
            print("   Have a productive day. Goodbye! 👋")
            print("=" * 45)
            break
        else:
            print("\n[Error] Invalid input. Please enter a number between 1 and 8.")
            pause()

if __name__ == "__main__":
    main()