# receipt.py
from utils import generate_receipt_number, get_timestamp, format_currency, print_divider
from datetime import datetime

def generate_receipt_file(cart, subtotal, vat, final_total, payment_info=None, customer=None):
    """
    Generates a printable .txt receipt file and returns the receipt number.
    """
    receipt_number = generate_receipt_number()
    timestamp = get_timestamp()
    
    lines = []
    lines.append("=" * 50)
    lines.append(f"{'KAPRI STORE':^50}")
    lines.append(f"{'123 Main Street, Kathmandu':^50}")
    lines.append(f"{'Phone: +977-9800000000':^50}")
    lines.append("=" * 50)
    lines.append(f"Receipt #: {receipt_number}")
    lines.append(f"Date:      {timestamp}")
    lines.append(f"Cashier:   Suman Kapri")
    if customer:
        lines.append(f"Customer:  {customer}")
    lines.append("-" * 50)
    lines.append(f"{'Item':<18} {'Qty':>5} {'Price':>8} {'Total':>10}")
    lines.append("-" * 50)
    
    # List each item
    for item in cart:
        name = item['name'][:17]  # Truncate long names
        lines.append(f"{name:<18} {item['quantity']:>5} {format_currency(item['price']):>8} {format_currency(item['total_cost']):>10}")
    
    lines.append("-" * 50)
    lines.append(f"{'Subtotal:':<35} {format_currency(subtotal):>12}")
    lines.append(f"{'VAT (13%):':<35} {format_currency(vat):>12}")
    lines.append(f"{'TOTAL:':<35} {format_currency(final_total):>12}")
    lines.append("=" * 50)
    
    # Payment info
    if payment_info:
        lines.append(f"Payment Method: {payment_info['method']}")
        if payment_info.get('cash_given'):
            lines.append(f"Cash Given:     {format_currency(payment_info['cash_given'])}")
            lines.append(f"Change:         {format_currency(payment_info['change'])}")
    
    lines.append("")
    lines.append(f"{'Thank you for shopping at Kapri Store!':^50}")
    lines.append(f"{'Visit us again soon. 🛒':^50}")
    lines.append("=" * 50)
    
    receipt_content = "\n".join(lines)
    
    # Print to terminal
    print("\n" + receipt_content)
    
    # Save to file
    filename = f"receipts/{receipt_number}.txt"
    import os
    os.makedirs("receipts", exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(receipt_content)
    
    print(f"\n✔ Receipt saved as: {filename}")
    return receipt_number


