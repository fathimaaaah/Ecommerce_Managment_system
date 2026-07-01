from tkinter import *
from db import connect
from customer import customer_panel
from sales import sales_panel

def admin_panel():

    win = Tk()
    win.title("Admin Dashboard")
    win.geometry("900x650")
    win.configure(bg="#f4f6f9")
    win.resizable(False, False)

    header = Frame(win, bg="#111827", height=70)
    header.pack(fill=X)

    Label(header,
          text="E‑Commerce Admin Dashboard",
          bg="#111827",
          fg="white",
          font=("Segoe UI", 18, "bold")
          ).pack(pady=18)

    container = Frame(win, bg="#f4f6f9")
    container.pack(fill=BOTH, expand=True, padx=20, pady=15)

    left = Frame(container, bg="white", padx=20, pady=20)
    left.pack(side=LEFT, fill=Y)

    Label(left, text="Product Management",
          bg="white",
          font=("Segoe UI", 14, "bold")).pack(pady=(0, 15))

    def field(label):
        Label(left, text=label, bg="white", anchor="w").pack(fill=X)
        e = Entry(left, font=("Segoe UI", 11))
        e.pack(fill=X, pady=5)
        return e

    pname = field("Product Name")
    price = field("Price")
    pid   = field("Product ID")
    qty   = field("Stock Quantity")

    # ---------------- DATABASE FUNCTIONS ----------------

    def add_product():
        db = connect()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO products(name, price) VALUES(%s, %s)",
            (pname.get(), price.get())
        )
        db.commit()
        show()

    def update_product():
        db = connect()
        cur = db.cursor()
        cur.execute(
            "UPDATE products SET name=%s, price=%s WHERE id=%s",
            (pname.get(), price.get(), pid.get())
        )
        db.commit()
        show()

    def delete_product():
        db = connect()
        cur = db.cursor()
        cur.execute(
            "DELETE FROM products WHERE id=%s",
            (pid.get(),)
        )
        db.commit()
        show()

    def add_stock():
        db = connect()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO stock(product_id, quantity) VALUES(%s, %s)",
            (pid.get(), qty.get())
        )
        db.commit()
        show()

    # ---------------- BUTTONS ----------------

    Button(left, text="Add Product",
           command=add_product,
           bg="#16a34a", fg="white").pack(fill=X, pady=5)

    Button(left, text="Update Product",
           command=update_product,
           bg="#f59e0b", fg="white").pack(fill=X, pady=5)

    Button(left, text="Delete Product",
           command=delete_product,
           bg="#dc2626", fg="white").pack(fill=X, pady=5)

    Button(left, text="Add Stock",
           command=add_stock,
           bg="#2563eb", fg="white").pack(fill=X, pady=5)

    # ---------------- RIGHT PANEL ----------------

    right = Frame(container, bg="white", padx=20, pady=20)
    right.pack(side=RIGHT, fill=BOTH, expand=True)

    Label(right, text="Products & Stock",
          bg="white",
          font=("Segoe UI", 14, "bold")).pack(pady=(0, 10))

    listbox = Listbox(right, font=("Consolas", 11))
    listbox.pack(fill=BOTH, expand=True)

    def show():
        listbox.delete(0, END)
        db = connect()
        cur = db.cursor()
        cur.execute("""
            SELECT products.id,
                   products.name,
                   products.price,
                   IFNULL(stock.quantity, 0)
            FROM products
            LEFT JOIN stock
            ON products.id = stock.product_id
        """)
        for row in cur.fetchall():
            listbox.insert(
                END,
                f"ID: {row[0]} | {row[1]} | ₹{row[2]} | Stock: {row[3]}"
            )

    footer = Frame(win, bg="#f4f6f9")
    footer.pack(pady=10)

    Button(footer, text="Manage Customers",
           command=customer_panel,
           width=22).pack(side=LEFT, padx=10)

    Button(footer, text="View Sales",
           command=sales_panel,
           width=22).pack(side=LEFT, padx=10)

    show()
    win.mainloop()
