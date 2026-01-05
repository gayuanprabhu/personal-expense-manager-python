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
root.title("Personal Expense Manager")
root.geometry("750x550")
root.configure(bg="#f4f6f8")

# ================= FUNCTIONS =================
def add_expense():
    desc = desc_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    today = date.today().isoformat()

    if not desc or not category or not amount:
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        amount = float(amount)
    except:
        messagebox.showerror("Error", "Amount must be numeric")
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
        messagebox.showwarning("Warning", "Select an expense")
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

    total_label.config(text=f"₹ {total:.2f}")

# ================= HEADER =================
header = tk.Label(
    root,
    text="Personal Expense Manager",
    font=("Segoe UI", 18, "bold"),
    bg="#f4f6f8",
    fg="#333"
)
header.pack(pady=10)

# ================= INPUT CARD =================
card = tk.Frame(root, bg="white", padx=15, pady=15, relief="groove", bd=1)
card.pack(padx=20, pady=10, fill="x")

tk.Label(card, text="Description", bg="white").grid(row=0, column=0, sticky="w")
desc_entry = tk.Entry(card, width=30)
desc_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(card, text="Category", bg="white").grid(row=0, column=2, sticky="w")
category_entry = tk.Entry(card, width=30)
category_entry.grid(row=0, column=3, padx=10, pady=5)

tk.Label(card, text="Amount (₹)", bg="white").grid(row=1, column=0, sticky="w")
amount_entry = tk.Entry(card, width=30)
amount_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Button(
    card,
    text="Add Expense",
    command=add_expense,
    bg="#1976d2",
    fg="white",
    width=18
).grid(row=1, column=3, pady=5)

# ================= TABLE =================
table_frame = tk.Frame(root, bg="white", padx=10, pady=10)
table_frame.pack(padx=20, pady=10, fill="both", expand=True)

columns = ("ID", "Description", "Category", "Amount", "Date")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(fill="both", expand=True)

# ================= FOOTER =================
footer = tk.Frame(root, bg="#f4f6f8")
footer.pack(fill="x", pady=10)

tk.Button(
    footer,
    text="Delete Selected",
    command=delete_expense,
    bg="#d32f2f",
    fg="white",
    width=18
).pack(side="left", padx=20)

total_label = tk.Label(
    footer,
    text="₹ 0.00",
    font=("Segoe UI", 14, "bold"),
    bg="#f4f6f8",
    fg="#2e7d32"
)
total_label.pack(side="right", padx=20)

load_expenses()
root.mainloop()
