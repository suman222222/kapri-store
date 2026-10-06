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
    """Calculates totals, prints receipt, and saves the transaction."""
    if not cart:
        print("\nNo items were added to the cart.")
        return

    print("\n" + "=" * 45)
    print("                 FINAL BILL")
    print("=" * 45)
    
    subtotal = 0.0
    
    print(f"\n{'Item':<15} {'SKU':<10} {'Price':<9} {'Qty':<5} {'Total':<10}")
    print("-" * 45)
    
    for item in cart:
        subtotal += item['total_cost']
        print(f"{item['name']:<15} {item['sku']:<10} ${item['price']:<8.2f} "
              f"{item['quantity']:<5} ${item['total_cost']:<9.2f}")

    vat = subtotal * 0.13
    final_total = subtotal + vat

    print("-" * 45)
    print(f"{'Subtotal:':<30} ${subtotal:.2f}")
    print(f"{'13% VAT:':<30} ${vat:.2f}")
    print(f"{'Final Total:':<30} ${final_total:.2f}")
    print("=" * 45)

    save_transaction(cart, subtotal, vat, final_total)
    
    input("\nPress Enter to return to the main menu...")

def save_transaction(cart, subtotal, vat, final_total):
    """Saves the current transaction to a history file."""
    history = load_json('transactions.json', [])
    
    transaction = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": cart,
        "subtotal": round(subtotal, 2),
        "vat": round(vat, 2),
        "final_total": round(final_total, 2)
    }
    
    history.append(transaction)
    save_json('transactions.json', history)
    print("✔ Transaction saved to history.")
    logging.info(f"New transaction completed. Total: ${final_total:.2f}")