# inventory.py
from utils import (
    print_header, load_json, save_json, pause, format_currency, print_divider
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def build_flat_inventory(inventory_data):
    """
    Converts nested inventory (category -> items) into a flat dictionary.
    Also injects the category name into each item for easy lookup.
    
    Returns:
        dict: { 'apple': {sku, price, cost, stock, unit, category}, ... }
    """
    flat = {}
    for category, items in inventory_data.items():
        for name, details in items.items():
            flat[name] = {**details, "category": category}
    return flat


# ============================================================
# 1. VIEW DATA (Transaction History - kept for menu compatibility)
# ============================================================

def view_data():
    """Displays all past transactions from the history file."""
    print_header("VIEW TRANSACTION HISTORY")
    
    history = load_json('transactions.json', [])
    
    if not history:
        print("\nNo transactions have been recorded yet.")
        pause()
        return

    print(f"\nTotal Transactions: {len(history)}")
    print(f"Total Revenue:      {format_currency(sum(t['final_total'] for t in history))}\n")
    print_divider("-", 50)
    
    # Show last 10 transactions
    for index, transaction in enumerate(reversed(history[-10:]), start=1):
        print(f"\n#{len(history) - index + 1} | {transaction['date']}")
        print(f"   Items: {len(transaction['items'])} | Total: {format_currency(transaction['final_total'])}")
        if 'payment' in transaction:
            print(f"   Payment: {transaction['payment'].get('method', 'N/A')}")
    
    if len(history) > 10:
        print(f"\n... and {len(history) - 10} more transactions.")
    
    pause()


# ============================================================
# 2. SEARCH PRODUCTS
# ============================================================

def search_products():
    """Search inventory by name, category, or SKU."""
    print_header("SEARCH PRODUCTS")
    
    inventory = load_json('products.json', {})
    if not inventory:
        print("\n[Error] Could not load inventory.")
        pause()
        return
    
    flat = build_flat_inventory(inventory)
    
    query = input("\nEnter search term (name, category, or SKU): ").strip().lower()
    if not query:
        print("No search term provided.")
        pause()
        return
    
    # Search across all fields
    results = [
        (name, data) for name, data in flat.items()
        if (query in name.lower()
            or query in data['category'].lower()
            or query in data['sku'].lower())
    ]
    
    if not results:
        print(f"\n❌ No products found matching '{query}'.")
    else:
        print(f"\n✔ Found {len(results)} product(s):\n")
        print(f"{'Item':<15} {'Category':<12} {'Price':>8} {'Stock':>7} {'SKU':>10}")
        print_divider("-", 60)
        for name, data in results:
            print(f"{name.capitalize():<15} {data['category']:<12} "
                  f"{format_currency(data['price']):>8} {data['stock']:>7} {data['sku']:>10}")
    
    pause()


# ============================================================
# 3. LOW STOCK ALERT
# ============================================================

def check_low_stock(threshold=20):
    """Displays all items below the stock threshold."""
    print_header("LOW STOCK ALERT")
    
    inventory = load_json('products.json', {})
    if not inventory:
        print("\n[Error] Could not load inventory.")
        pause()
        return
    
    flat = build_flat_inventory(inventory)
    
    # List comprehension to filter low-stock items
    low_stock_items = [
        (name, data) for name, data in flat.items()
        if data['stock'] < threshold
    ]
    
    if not low_stock_items:
        print(f"\n✅ All items have healthy stock (>= {threshold} units).")
    else:
        print(f"\n⚠️  {len(low_stock_items)} item(s) need restocking (below {threshold} units):\n")
        print(f"{'Item':<15} {'Category':<12} {'Stock':>7} {'SKU':>10}  Status")
        print_divider("-", 60)
        
        # Sort by lowest stock first
        low_stock_items.sort(key=lambda x: x[1]['stock'])
        
        for name, data in low_stock_items:
            status = "🔴 CRITICAL" if data['stock'] < 10 else "🟡 LOW"
            print(f"{name.capitalize():<15} {data['category']:<12} "
                  f"{data['stock']:>7} {data['sku']:>10}  {status}")
    
    pause()


# ============================================================
# 4. ADMIN: RESTOCK INVENTORY
# ============================================================

def admin_restock():
    """Admin function to add stock to items."""
    print_header("ADMIN: RESTOCK INVENTORY")
    
    inventory = load_json('products.json', {})
    if not inventory:
        print("\n[Error] Could not load inventory.")
        pause()
        return
    
    # Show current inventory grouped by category
    print("\n--- Current Inventory ---")
    for category, items in inventory.items():
        print(f"\n📦 {category.upper()}")
        for name, details in items.items():
            print(f"  • {name.capitalize():<15} Stock: {details['stock']:<5} {details['unit']}")
    
    print_divider("-", 50)
    item_name = input("\nEnter item name to restock (or 'cancel'): ").strip().lower()
    
    if item_name == 'cancel' or not item_name:
        print("Restock cancelled.")
        pause()
        return
    
    # Find the item across all categories
    found_category = None
    for category, items in inventory.items():
        if item_name in items:
            found_category = category
            break
    
    if not found_category:
        print(f"\n❌ Item '{item_name}' not found in inventory.")
        pause()
        return
    
    current_stock = inventory[found_category][item_name]['stock']
    print(f"\nCurrent stock of {item_name.capitalize()}: {current_stock}")
    
    try:
        amount = int(input(f"Enter quantity to add: ").strip())
        if amount <= 0:
            print("❌ Amount must be a positive number.")
            pause()
            return
        
        inventory[found_category][item_name]['stock'] += amount
        new_stock = inventory[found_category][item_name]['stock']
        
        save_json('products.json', inventory)
        
        print(f"\n✔ Successfully restocked!")
        print(f"   Item:         {item_name.capitalize()}")
        print(f"   Added:        {amount} units")
        print(f"   New Stock:    {new_stock} units")
        
    except ValueError:
        print("❌ Invalid number. Please enter a whole number.")
    
    pause()


# ============================================================
# 5. ADMIN: DELETE DATA (Placeholder for now)
# ============================================================

def delete_data():
    """Placeholder for deleting data."""
    print_header("DELETE DATA")
    print("\nThis feature will allow you to delete or void items in the future.")
    print("Currently, use the Admin Panel to delete transactions.")
    pause()