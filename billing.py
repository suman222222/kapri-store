# billing.py
from datetime import datetime
from utils import print_header, get_valid_number, load_json, save_json, logging

class OutOfStockError(Exception):
    """Custom exception raised when requested quantity exceeds available stock."""
    pass

class ItemNotFoundError(Exception):
    """Custom exception raised when an item is not in the inventory."""
    pass

def build_flat_inventory(inventory_data):
    """
    Converts the nested category-based inventory into a flat dictionary
    for easy lookups: { 'apple': {...}, 'milk': {...} }
    """
    flat_inventory = {}
    for category, items in inventory_data.items():
        for item_name, details in items.items():
            flat_inventory[item_name] = details
    return flat_inventory

def display_inventory(inventory):
    """Displays the available inventory grouped by category."""
    print("\n--- AVAILABLE INVENTORY ---")
    for category, items in inventory.items():
        print(f"\n📦 {category.upper()}")
        for item_name, details in items.items():
            stock_status = "✅" if details['stock'] > 20 else "⚠️ Low Stock"
            print(f"  • {item_name.capitalize():<12} ${details['price']:<6.2f} "
                  f"({details['unit']}) - Stock: {details['stock']} {stock_status}")
    print("\n" + "-" * 45)

def add_items():
    """Main billing loop with stock checking and inventory validation."""
    print_header("KAPRI STORE - BILLING SYSTEM")
    
    inventory_data = load_json('products.json', {})
    if not inventory_data:
        print("\n[Error] Inventory is empty. Please contact an administrator.")
        input("Press Enter to return...")
        return

    # Flatten for quick lookups
    flat_inventory = build_flat_inventory(inventory_data)
    
    display_inventory(inventory_data)

    shopping_cart = []
    
    while True:
        print("\n--- Enter Item Details ---")
        item_name = input("Enter item name (or 'done' to finish): ").strip().lower()
        
        if item_name == 'done':
            break

        try:
            # Check if item exists
            if item_name not in flat_inventory:
                raise ItemNotFoundError(f"'{item_name}' is not in our inventory.")

            item_data = flat_inventory[item_name]
            item_price = item_data['price']
            available_stock = item_data['stock']

            item_quantity = get_valid_number(f"Enter quantity for {item_name} (Available: {available_stock}): ", is_float=False)

            # Check stock
            if item_quantity > available_stock:
                raise OutOfStockError(f"Only {available_stock} units of '{item_name}' available in stock.")

            total_cost = item_price * item_quantity

            item_dict = {
                "name": item_name.capitalize(),
                "sku": item_data['sku'],
                "price": item_price,
                "quantity": item_quantity,
                "total_cost": total_cost
            }
            
            shopping_cart.append(item_dict)
            print(f"✔ Added {item_quantity}x {item_name.capitalize()} to cart. Subtotal: ${total_cost:.2f}")

            # Optional: Deduct stock immediately (in-memory)
            item_data['stock'] -= item_quantity

        except ItemNotFoundError as e:
            print(f"[Error] {e}")
            logging.warning(f"ItemNotFoundError: {e}")
        except OutOfStockError as e:
            print(f"[Error] {e}")
            logging.warning(f"OutOfStockError: {e}")

        add_another = input("Add another item? (yes/no): ").strip().lower()
        if add_another != 'yes':
            break

    if shopping_cart:
        # Save the updated inventory (stock deductions) back to the JSON file
        save_json('products.json', inventory_data)
        process_bill(shopping_cart)

def process_bill(cart):
    """Calculates totals, prints receipt, saves transaction."""
    if not cart:
        print("\nNo items were added to the cart.")
        return

    subtotal = sum(item['total_cost'] for item in cart)
    vat = subtotal * 0.13
    final_total = subtotal + vat

    # Ask for payment method
    print("\n--- Payment ---")
    print(f"Total to pay: ${final_total:.2f}")
    print("1. Cash")
    print("2. Card")
    payment_choice = input("Select payment method (1/2): ").strip()
    
    payment_info = {"method": "Card"}
    
    if payment_choice == '1':
        payment_info["method"] = "Cash"
        try:
            cash = float(input(f"Cash received: $"))
            if cash < final_total:
                print(f"[Error] Insufficient cash. Need at least ${final_total:.2f}")
                return
            payment_info["cash_given"] = cash
            payment_info["change"] = cash - final_total
        except ValueError:
            print("[Error] Invalid cash amount.")
            return
    
    # Optional: customer name for loyalty
    customer = input("Customer name (or press Enter to skip): ").strip() or None
    
    # Generate receipt
    from receipt import generate_receipt_file
    receipt_number = generate_receipt_file(cart, subtotal, vat, final_total, payment_info, customer)
    
    # Save to history
    save_transaction(cart, subtotal, vat, final_total, receipt_number, payment_info)
    
    input("\nPress Enter to return to main menu...")

def save_transaction(cart, subtotal, vat, final_total, receipt_number, payment_info):
    """Saves the current transaction with full details."""
    history = load_json('transactions.json', [])
    
    transaction = {
        "receipt_number": receipt_number,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": cart,
        "subtotal": round(subtotal, 2),
        "vat": round(vat, 2),
        "final_total": round(final_total, 2),
        "payment": payment_info
    }
    
    history.append(transaction)
    save_json('transactions.json', history)
    logging.info(f"Transaction {receipt_number} saved. Total: ${final_total:.2f}")