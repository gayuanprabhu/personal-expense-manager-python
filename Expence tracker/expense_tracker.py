import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date

# ================= DATABASE =================
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    category TEXT,
    amount REAL,
    expense_date TEXT
)
""")
conn.commit()

# ================= GUI =================
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("600x550")
root.config(bg="white")

# ================= FUNCTIONS =================
def add_expense():
    desc = desc_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    today = date.today().isoformat()

    if desc == "" or category == "" or amount == "":
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        amount = float(amount)
    except:
        messagebox.showerror("Error", "Amount must be a number")
        return

    cursor.execute(
        "INSERT INTO expenses (description, category, amount, expense_date) VALUES (?, ?, ?, ?)",
        (desc, category, amount, today)
    )
    conn.commit()

    desc_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

    load_expenses()

def delete_expense():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select an expense first")
        return

    expense_id = tree.item(selected[0])["values"][0]
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()

    load_expenses()

def load_expenses():
    tree.delete(*tree.get_children())

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    total = 0
    for row in rows:
        tree.insert("", "end", values=row)
        total += row[3]

    total_label.config(text=f"Total: ₹{total:.2f}")

# ================= INPUT =================
tk.Label(root, text="Description", bg="white").pack()
desc_entry = tk.Entry(root, width=45)
desc_entry.pack()

tk.Label(root, text="Category", bg="white").pack()
category_entry = tk.Entry(root, width=45)
category_entry.pack()

tk.Label(root, text="Amount (₹)", bg="white").pack()
amount_entry = tk.Entry(root, width=45)
amount_entry.pack()

tk.Button(
    root, text="Add Expense",
    command=add_expense,
    bg="green", fg="white", width=20
).pack(pady=10)

# ================= TABLE =================
columns = ("ID", "Description", "Category", "Amount", "Date")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(pady=10, fill="x")

tk.Button(
    root, text="Delete Selected Expense",
    command=delete_expense,
    bg="red", fg="white", width=25
).pack(pady=5)

# ================= TOTAL =================
total_label = tk.Label(
    root, text="Total: ₹0.00",
    font=("Arial", 12, "bold"),
    bg="white", fg="green"
)
total_label.pack(pady=10)

load_expenses()
root.mainloop()
