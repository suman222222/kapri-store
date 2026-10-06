# reports.py
from datetime import datetime
from collections import Counter
from utils import print_header, load_json, pause, format_currency

def daily_sales_report():
    """Shows today's sales, revenue, profit, and top-selling items."""
    print_header("DAILY SALES REPORT")
    
    history = load_json('transactions.json', [])
    inventory = load_json('products.json', {})
    
    if not history:
        print("\nNo transactions found.")
        pause()
        return
    
    today = datetime.now().strftime("%Y-%m-%d")
    todays_transactions = [t for t in history if t['date'].startswith(today)]
    
    if not todays_transactions:
        print(f"\nNo sales recorded today ({today}).")
        pause()
        return
    
    # Calculate totals
    total_revenue = sum(t['final_total'] for t in todays_transactions)
    total_subtotal = sum(t['subtotal'] for t in todays_transactions)
    total_vat = sum(t['vat'] for t in todays_transactions)
    
    # Calculate profit (revenue - cost of goods sold)
    total_profit = 0.0
    item_sales = Counter()  # Track how many of each item was sold
    
    # Build a cost lookup from inventory
    cost_lookup = {}
    for category, items in inventory.items():
        for name, details in items.items():
            cost_lookup[name.lower()] = details['cost']
    
    for transaction in todays_transactions:
        for item in transaction['items']:
            item_name = item['name'].lower()
            cost_per_unit = cost_lookup.get(item_name, 0)
            total_profit += (item['price'] - cost_per_unit) * item['quantity']
            item_sales[item['name']] += item['quantity']
    
    # Display report
    print(f"\n📅 Date: {today}")
    print(f"🧾 Total Transactions: {len(todays_transactions)}")
    print(f"📦 Total Items Sold: {sum(item_sales.values())}")
    print("-" * 50)
    print(f"💰 Gross Revenue:    {format_currency(total_revenue)}")
    print(f"   Subtotal:         {format_currency(total_subtotal)}")
    print(f"   VAT Collected:    {format_currency(total_vat)}")
    print(f"📈 Estimated Profit: {format_currency(total_profit)}")
    print("-" * 50)
    
    # Top 5 selling items
    print("\n🔥 Top 5 Best Sellers Today:")
    for rank, (item, qty) in enumerate(item_sales.most_common(5), start=1):
        print(f"   {rank}. {item:<15} - {qty} units sold")
    
    pause()

def full_transaction_history():
    """Shows all past transactions (was the old view_data function)."""
    print_header("TRANSACTION HISTORY")
    
    history = load_json('transactions.json', [])
    
    if not history:
        print("\nNo transactions have been recorded yet.")
        pause()
        return
    
    print(f"\nTotal Transactions: {len(history)}")
    print(f"Total Revenue: {format_currency(sum(t['final_total'] for t in history))}\n")
    
    # Show last 10 transactions
    print("--- Last 10 Transactions ---")
    for index, transaction in enumerate(reversed(history[-10:]), start=1):
        print(f"\n#{len(history) - index + 1} | {transaction['date']}")
        print(f"   Items: {len(transaction['items'])} | Total: {format_currency(transaction['final_total'])}")
    
    pause()

def category_performance():
    """Shows which categories sell best."""
    print_header("CATEGORY PERFORMANCE")
    
    history = load_json('transactions.json', [])
    inventory = load_json('products.json', {})
    
    if not history:
        print("\nNo data available.")
        pause()
        return
    
    # Build category lookup
    category_lookup = {}
    for category, items in inventory.items():
        for name in items.keys():
            category_lookup[name.lower()] = category
    
    category_revenue = {}
    category_units = {}
    
    for transaction in history:
        for item in transaction['items']:
            cat = category_lookup.get(item['name'].lower(), 'uncategorized')
            category_revenue[cat] = category_revenue.get(cat, 0) + item['total_cost']
            category_units[cat] = category_units.get(cat, 0) + item['quantity']
    
    # Sort by revenue
    sorted_categories = sorted(category_revenue.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\n{'Category':<15} {'Revenue':>12} {'Units Sold':>12}")
    print("-" * 45)
    for cat, revenue in sorted_categories:
        print(f"{cat.capitalize():<15} {format_currency(revenue):>12} {category_units[cat]:>12}")
    
    pause()