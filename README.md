# 🛒 Kapri Store - Billing & Management System

A robust, command-line based Point of Sale (POS) and billing system designed for **Kapri Store**.

This project was built to transition from basic Python scripting to **professional modular software architecture**. It separates concerns into different modules, utilizes advanced data structures, and implements robust error handling to ensure the system never crashes due to bad user input.

---

## 📖 Table of Contents
- [Features](#-features)
- [Who Uses Kapri Store?](#-who-uses-kapri-store)
- [Project Structure](#-project-structure)
- [How to Run](#-how-to-run)
- [Technical Concepts](#-technical-concepts-demonstrated)
- [Roadmap](#-future-roadmap)
- [Author](#-author)

---

## ✨ Features

- **Modular Architecture:** Logic is separated into distinct files (`billing.py`, `inventory.py`, `reports.py`, `receipt.py`, `utils.py`) for maintainability and scalability.

- **50+ Product Inventory:** Categorized groceries with SKUs, cost prices, retail prices, and live stock tracking.

- **Dynamic Billing System:** Users can add multiple items continuously. The system calculates the total cost per item, subtotal, applies a 13% VAT, and generates a formatted receipt.

- **Printable Receipts:** Every transaction is saved as a `.txt` receipt file in the `receipts/` folder.

- **Robust Exception Handling:** Custom exceptions (`ItemNotFoundError`, `OutOfStockError`) ensure the program gracefully handles invalid inputs without crashing.
- **Search & Filter:** Search products by name, category, or SKU.
- **Low Stock Alerts:** Automatically flags items that need restocking.
- **Daily Sales Reports:** View revenue, profit, and top-selling items for the current day.
- **Category Performance Analytics:** See which categories of products sell best.
- **Admin Panel:** Secure restocking and transaction management.
- **Logging System:** All critical actions are logged to `kapri_store.log` for auditing.

---

## 👥 Who Uses Kapri Store?

Kapri Store is designed to be useful at **three different scales**, depending on the size of the business. Here's how it works in each real-world scenario:

### Scenario 1: Small Kirana Store (Current CLI Version)

**Who uses it:** The shop owner and 1–2 cashiers.

**How it works:**
1. The **owner** opens `python main.py` on the shop's computer each morning.
2. The **cashier** selects **Option 1 (New Sale)** for each customer.
3. The cashier types the item name (`apple`, `milk`) → the system verifies stock.
4. The cashier enters quantity → the system calculates the total plus 13% VAT.
5. The cashier takes cash or card → the system calculates the change.
6. The system **prints the receipt**, saves a `.txt` file, and updates stock in `products.json`.
7. At closing time, the **owner** runs **Option 4 (Daily Report)** to see revenue and profit.

**Real-world value:**
- ✅ No more manual calculations on paper
- ✅ Live stock tracking (no manual counting)
- ✅ Automatic VAT calculation
- ✅ Professional printed receipts
- ✅ End-of-day profit reports

**Hardware needed:** A basic laptop/desktop with Python installed. No internet required.

---

### 🏬 Scenario 2: Multi-Cashier Store (Phase 3 — MySQL Integration)

When the store grows to have **multiple cashiers** and a **manager**, a single laptop isn't enough. This is where we introduce a central MySQL database so multiple terminals share the same data in real-time.

**How it would work:**
- Each cashier runs their own instance of `main.py` on their own terminal.
- All terminals read/write to a **shared MySQL database**.
- The manager has a **separate login** with admin privileges (restock, reports, refunds).
- Role-based access prevents cashiers from modifying inventory directly.

**Real-world value:**
- ✅ Multiple cashiers work simultaneously without data conflicts
- ✅ Real-time synced sales across all terminals
- ✅ Manager sees live sales from anywhere
- ✅ Secure login system

---

### 🌐 Scenario 3: Modern Web Store (Phase 5 — Full-Stack Version)

This is the ultimate goal — turning Kapri Store into a **full-stack web application** accessible from any browser.

**How it works:**
- A **Flask API** runs on a server, exposing endpoints like `/api/products`, `/api/cart`, `/api/checkout`.

- Customers visit `store.kapri.com` on their phone or laptop, browse products, and order online.

- Data is stored in a **cloud-hosted MySQL database**.

- The owner has a **mobile-friendly dashboard** to monitor sales, stock, and profit in real-time.

**Real-world value:**
- ✅ Customers can order from anywhere
- ✅ Owner manages the store from their phone
- ✅ No installation required — just a link
- ✅ Scales to thousands of daily orders

---

### 🎯 Why This Matters

A program is not defined by how fancy it looks — it's defined by **whether it solves a real problem**.

| Version | Solves Which Problem? | Who Uses It? |
|---|---|---|
| **CLI App (Current)** | Small shop tracking sales + stock | 1 owner, 1 cashier |
| **MySQL Version (Phase 3)** | Multi-cashier, shared data | Small team |
| **Web Version (Phase 5)** | Customer self-service + remote management | Thousands |

Your current CLI app **is already useful**. A real small shop can run it today and benefit immediately.

---

## 📂 Project Structure

```text
kapri-store/
│
├── main.py             # Entry point. Contains the main menu and routing logic.
├── billing.py          # Billing logic, stock validation, and checkout process.
├── inventory.py        # Product search, low-stock alerts, and admin restocking.
├── reports.py          # Daily sales, profit analysis, and category performance.
├── receipt.py          # Receipt generation (terminal + .txt file).
├── utils.py            # Helper functions (JSON I/O, input validation, logging).
├── products.json       # The store's inventory database (categories, SKUs, stock).
├── transactions.json   # Auto-generated. Stores all past transactions.
├── kapri_store.log     # Auto-generated. Audit trail of system events.
├── receipts/           # Auto-generated. Stores .txt receipt files.
├── .gitignore          # Files excluded from version control.
└── README.md           # Project documentation.
🚀 How to Run the Application
Prerequisites
Python 3.8+ installed on your system.

No external libraries required (uses only Python standard library).

Steps
Clone the repository:

bash
git clone https://github.com/your-username/kapri-store.git
Navigate to the project directory:

bash
cd kapri-store

Run the main program:

bash
python main.py
(On Windows, if python is not recognized, use py main.py)

Available Menu Options
Option	Feature
1	🛒 New Sale (Billing)
2	🔍 Search Products
3	📊 View Transaction History
4	📈 Daily Sales Report
5	📦 Category Performance
6	⚠️ Low Stock Alerts
7	🔧 Admin Panel (Restock)
8	🚪 Exit



🧠 Technical Concepts Demonstrated
This project serves as a showcase of core and advanced Python concepts:

Functions & Modularity: Complex problems are broken into small, reusable functions across multiple files.

Loops & Control Flow: while loops for continuous menu execution; for loops for iterating over cart items.

Data Structures:

Lists: Storing the shopping cart.

Dictionaries: Representing individual items and inventory categories.

2D Lists (List of Dictionaries): Storing full transaction history.

Counter (collections): Tracking best-selling items.

Exception Handling: Custom exceptions (ItemNotFoundError, OutOfStockError) plus try...except for input validation.

File I/O: Reading/writing JSON files with json module; saving receipts with open().

String Formatting: F-strings with alignment and currency formatting (e.g., ${:.2f}).

Built-in Modules: os, json, logging, datetime, collections, random.

List Comprehensions: Filtering low-stock items, searching products.

Sorting with Lambdas: Sorting categories and low-stock items.

Logging: Professional audit trail using the logging module.

🔮 Future Roadmap
☑ Phase 1: Modular CLI billing system with inventory and reports.
□ Phase 2: Customer loyalty system with points tracking.
□ Phase 3: Migrate from JSON to MySQL for multi-terminal support.
□ Phase 4: Build a Flask REST API to expose store logic.
□ Phase 5: Build a web frontend (HTML/CSS/JS) for customers and management.
□ Phase 6: Barcode scanner simulation.
□ Phase 7: User authentication (Admin/Cashier roles).
□ Phase 8: Deploy to the cloud (accessible from any phone/laptop).


👨‍💻 Author
Suman Kapri
Second-Year Computer Science Student
Passionate about Full Stack Development, UI/UX, and Software Architecture.

