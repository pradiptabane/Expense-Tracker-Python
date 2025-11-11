#!/usr/bin/env python3
"""
Personal Expense Tracker (CLI)
Features:
- Add expense (date, category, amount, description)
- View all expenses
- Show summary: total and category-wise totals
- Data persisted in a CSV file (expenses.csv)
"""
import csv
import os
from datetime import datetime

CSV_FILE = "expenses.csv"
FIELDNAMES = ["id","date","category","amount","description"]

def ensure_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

def next_id():
    ensure_csv()
    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        ids = [int(row["id"]) for row in reader]
        return max(ids)+1 if ids else 1

def add_expense():
    try:
        date_str = input("Date (YYYY-MM-DD) [leave blank for today]: ").strip()
        if not date_str:
            date_obj = datetime.today()
        else:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        category = input("Category (e.g., Food, Travel, Bills): ").strip() or "Misc"
        amount_str = input("Amount: ").strip()
        amount = float(amount_str)
        description = input("Description (optional): ").strip()
    except ValueError:
        print("Invalid input. Please try again.")
        return

    row = {
        "id": next_id(),
        "date": date_obj.strftime("%Y-%m-%d"),
        "category": category,
        "amount": f"{amount:.2f}",
        "description": description
    }
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(row)
    print("Expense added.")

def view_expenses():
    ensure_csv()
    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        print("No expenses recorded yet.")
        return
    print(f"\n{'ID':<4} {'Date':<10} {'Category':<12} {'Amount':>8}  Description")
    print("-"*60)
    for r in rows:
        print(f"{r['id']:<4} {r['date']:<10} {r['category']:<12} {float(r['amount']):>8.2f}  {r['description']}")
    print()

def summary():
    ensure_csv()
    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        total = 0.0
        by_cat = {}
        for r in reader:
            amt = float(r["amount"])
            total += amt
            by_cat[r["category"]] = by_cat.get(r["category"], 0.0) + amt
    print("\nExpense Summary")
    print("-"*30)
    print(f"Total spent: {total:.2f}")
    print("\nBy category:")
    for cat, amt in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"  {cat:<12} {amt:>8.2f}")
    print()

def export_report(filename="expense_report.txt"):
    ensure_csv()
    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    with open(filename, "w") as f:
        f.write("Expense Report\n")
        f.write("="*40+"\n")
        for r in rows:
            f.write(f"{r['date']} | {r['category']:<10} | {r['amount']:>8} | {r['description']}\n")
    print(f"Report exported to {filename}")

def menu():
    while True:
        print("\nPersonal Expense Tracker")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Summary")
        print("4. Export report to text file")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            summary()
        elif choice == "4":
            fname = input("Filename (default: expense_report.txt): ").strip() or "expense_report.txt"
            export_report(fname)
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    menu()
