# billing.py
from utils import print_header

def get_valid_number(prompt, is_float=True):
    """Helper function to validate numeric inputs (prices and quantities)."""
    while True:
        try:
            value = float(input(prompt)) if is_float else int(input(prompt))
            if value < 0:
                print("Input cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def add_items():
    """Loops to gather item data and stores it in a 2D List."""
    shopping_cart = [] # This is our 2D List
    
    print_header("KAPRI STORE - BILLING SYSTEM")
    
    while True:
        print("\n--- Enter Item Details ---")
        item_name = input("Enter item name: ").strip()
        
        # Using our helper function for validation
        item_price = get_valid_number(f"Enter price for {item_name}: $", is_float=True)
        item_quantity = get_valid_number(f"Enter quantity for {item_name}: ", is_float=False)

        total_cost = item_price * item_quantity

        # Using a Dictionary to represent the item, then appending it to our List
        item_dict = {
            "name": item_name,
            "price": item_price,
            "quantity": item_quantity,
            "total_cost": total_cost
        }
        
        shopping_cart.append(item_dict)

        add_another = input("Do you want to add another item? (yes/no): ").strip().lower()
        if add_another == 'no':
            break
        elif add_another != 'yes':
            print("Invalid input. Assuming 'no' and proceeding.")
            break

    # Once the loop breaks, process the final bill
    process_bill(shopping_cart)

def process_bill(cart):
    """Calculates totals and prints the final receipt."""
    if not cart:
        print("\nNo items were added to the cart.")
        return

    print("\n" + "=" * 40)
    print("               FINAL BILL")
    print("=" * 40)
    
    print("\nItems purchased:")
    for item in cart:
        print(f"- {item['name']}")

    subtotal = 0.0
    
    print("\n--- Detailed Receipt ---")
    print(f"{'Item':<15} {'Price':<10} {'Qty':<5} {'Total':<10}")
    print("-" * 40)
    
    # Iterate through the 2D List of dictionaries
    for item in cart:
        subtotal += item['total_cost']
        print(f"{item['name']:<15} ${item['price']:<9.2f} {item['quantity']:<5} ${item['total_cost']:<9.2f}")

    vat = subtotal * 0.13
    final_total = subtotal + vat

    print("-" * 40)
    print(f"{'Subtotal:':<30} ${subtotal:.2f}")
    print(f"{'13% VAT:':<30} ${vat:.2f}")
    print(f"{'Final Total:':<30} ${final_total:.2f}")
    print("=" * 40)
    input("\nPress Enter to return to the main menu...")