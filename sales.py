from tkinter import *
from db import connect


def sales_panel():

    win = Tk()
    win.title("Sales Management")
    win.geometry("900x600")
    win.configure(bg="#f4f6f9")
    win.resizable(False, False)

    # ================= HEADER =================
    header = Frame(win, bg="#111827", height=70)
    header.pack(fill=X)

    Label(header,
          text="Sales Management",
          bg="#111827",
          fg="white",
          font=("Segoe UI", 18, "bold")
          ).pack(pady=18)

    # ================= MAIN FRAME =================
    container = Frame(win, bg="#f4f6f9")
    container.pack(fill=BOTH, expand=True, padx=20, pady=15)

    left = Frame(container, bg="white", padx=20, pady=20)
    left.pack(side=LEFT, fill=Y, padx=10)

    right = Frame(container, bg="white", padx=20, pady=20)
    right.pack(side=RIGHT, fill=BOTH, expand=True, padx=10)

    # ================= LEFT SIDE (CREATE SALE) =================
    Label(left, text="Create New Sale",
          bg="white",
          font=("Segoe UI", 14, "bold")
          ).pack(pady=(0, 15))

    Label(left, text="Customer ID", bg="white").pack(anchor="w")
    customer_id = Entry(left)
    customer_id.pack(fill=X, pady=5)

    Label(left, text="Total Amount", bg="white").pack(anchor="w")
    total = Entry(left)
    total.pack(fill=X, pady=5)

    def create_sale():
        db = connect()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO sales(customer_id, total) VALUES(%s, %s)",
            (customer_id.get(), total.get())
        )
        db.commit()
        show_sales()

    Button(left,
           text="Add Sale",
           command=create_sale,
           bg="#16a34a",
           fg="white",
           font=("Segoe UI", 10, "bold")
           ).pack(fill=X, pady=15)

    # ================= RIGHT SIDE (REPORT) =================
    Label(right, text="Sales Report",
          bg="white",
          font=("Segoe UI", 14, "bold")
          ).pack(pady=(0, 10))

    listbox = Listbox(right, font=("Consolas", 11))
    listbox.pack(fill=BOTH, expand=True)

    def show_sales():
        listbox.delete(0, END)
        db = connect()
        cur = db.cursor()
        cur.execute("""
            SELECT sales.id,
                   customers.name,
                   sales.total,
                   sales.sale_date
            FROM sales
            JOIN customers
            ON sales.customer_id = customers.id
            ORDER BY sales.sale_date DESC
        """)
        for r in cur.fetchall():
            listbox.insert(
                END,
                f"Sale ID: {r[0]} | Customer: {r[1]} | ₹{r[2]} | {r[3]}"
            )

    show_sales()
    win.mainloop()
