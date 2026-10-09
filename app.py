import sqlite3
import datetime
import matplotlib.pyplot as plt

DB_NAME = "expenses.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL
        )
    """)
    conn.commit()
    conn.close()

# Add expense
def add_expense(category, amount):
    date = datetime.date.today().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)",
                   (date, category, amount))
    conn.commit()
    conn.close()
    print("✅ Expense added successfully!")

# View all expenses
def view_expenses():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()
    print("\n--- All Expenses ---")
    for row in rows:
        print(row)

# Update expense
def update_expense(expense_id, new_category, new_amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE expenses SET category=?, amount=? WHERE id=?",
                   (new_category, new_amount, expense_id))
    conn.commit()
    conn.close()
    print("✏️ Expense updated successfully!")

# Delete expense
def delete_expense(expense_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()
    print("🗑️ Expense deleted successfully!")

# Summary report
def summary_report():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    rows = cursor.fetchall()
    conn.close()

    print("\n--- Expense Summary ---")
    categories = []
    totals = []
    for row in rows:
        categories.append(row[0])
        totals.append(row[1])
        print(f"{row[0]}: ₹{row[1]}")

    # Visualization
    plt.pie(totals, labels=categories, autopct="%1.1f%%")
    plt.title("Expenses by Category")
    plt.show()

# Main menu
def main():
    init_db()
    while True:
        print("\n--- Smart Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Summary Report")
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            category = input("Enter category: ")
            amount = float(input("Enter amount: "))
            add_expense(category, amount)
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            expense_id = int(input("Enter expense ID to update: "))
            new_category = input("Enter new category: ")
            new_amount = float(input("Enter new amount: "))
            update_expense(expense_id, new_category, new_amount)
        elif choice == "4":
            expense_id = int(input("Enter expense ID to delete: "))
            delete_expense(expense_id)
        elif choice == "5":
            summary_report()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
