# inventory.py
from utils import print_header, load_json

def view_data():
    """Displays all past transactions from the history file."""
    print_header("VIEW TRANSACTION HISTORY")
    
    history = load_json('transactions.json', [])
    
    if not history:
        print("\nNo transactions have been recorded yet.")
        input("\nPress Enter to return to the main menu...")
        return

    print(f"\nTotal Transactions: {len(history)}\n")
    
    for index, transaction in enumerate(history, start=1):
        print(f"--- Transaction #{index} ---")
        print(f"Date: {transaction['date']}")
        print(f"Items: {len(transaction['items'])}")
        print(f"Final Total: ${transaction['final_total']:.2f}")
        print("-" * 30)
    
    input("\nPress Enter to return to the main menu...")

def delete_data():
    """Placeholder for deleting data."""
    print_header("DELETE DATA")
    print("This feature will allow you to delete or void items in the future.")
    input("\nPress Enter to return to the main menu...")