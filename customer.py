from tkinter import *
from db import connect


def customer_panel():

    # ================= WINDOW =================
    win = Tk()
    win.title("Customer Management")
    win.geometry("850x600")
    win.configure(bg="#f4f6f9")
    win.resizable(False, False)

    # ================= HEADER =================
    header = Frame(win, bg="#111827", height=70)
    header.pack(fill=X)

    Label(
        header,
        text="Customer Management",
        bg="#111827",
        fg="white",
        font=("Segoe UI", 18, "bold")
    ).pack(pady=18)

    # ================= MAIN CONTAINER =================
    container = Frame(win, bg="#f4f6f9")
    container.pack(fill=BOTH, expand=True, padx=20, pady=15)

    # ================= LEFT PANEL =================
    left = Frame(container, bg="white", padx=20, pady=20)
    left.pack(side=LEFT, fill=Y)

    Label(left, text="Customer Details",
          bg="white",
          font=("Segoe UI", 14, "bold")).pack(pady=(0, 15))

    def field(label):
        Label(left, text=label, bg="white", anchor="w").pack(fill=X)
        e = Entry(left, font=("Segoe UI", 11))
        e.pack(fill=X, pady=5)
        return e

    name = field("Name")
    phone = field("Phone")
    email = field("Email")
    address = field("Address")
    cid = field("Customer ID")

    # ================= DATABASE FUNCTIONS =================
    def add_customer():
        db = connect()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO customers(name, phone, email, address) VALUES(%s, %s, %s, %s)",
            (name.get(), phone.get(), email.get(), address.get())
        )
        db.commit()
        show()

    def update_customer():
        db = connect()
        cur = db.cursor()
        cur.execute(
            "UPDATE customers SET name=%s, phone=%s, email=%s, address=%s WHERE id=%s",
            (name.get(), phone.get(), email.get(), address.get(), cid.get())
        )
        db.commit()
        show()

    def delete_customer():
        db = connect()
        cur = db.cursor()
        cur.execute(
            "DELETE FROM customers WHERE id=%s",
            (cid.get(),)
        )
        db.commit()
        show()

    # ================= BUTTONS =================
    Button(left, text="Add Customer",
           command=add_customer,
           bg="#16a34a", fg="white",
           font=("Segoe UI", 10, "bold"),
           relief=FLAT).pack(fill=X, pady=5)

    Button(left, text="Update Customer",
           command=update_customer,
           bg="#f59e0b", fg="white",
           font=("Segoe UI", 10, "bold"),
           relief=FLAT).pack(fill=X, pady=5)

    Button(left, text="Delete Customer",
           command=delete_customer,
           bg="#dc2626", fg="white",
           font=("Segoe UI", 10, "bold"),
           relief=FLAT).pack(fill=X, pady=5)

    # ================= RIGHT PANEL =================
    right = Frame(container, bg="white", padx=20, pady=20)
    right.pack(side=RIGHT, fill=BOTH, expand=True)

    Label(right, text="Customer List",
          bg="white",
          font=("Segoe UI", 14, "bold")).pack(pady=(0, 10))

    listbox = Listbox(
        right,
        font=("Consolas", 11),
        height=18,
        width=60
    )
    listbox.pack(fill=BOTH, expand=True)

    def show():
        listbox.delete(0, END)
        db = connect()
        cur = db.cursor()
        cur.execute("SELECT * FROM customers")
        for r in cur.fetchall():
            listbox.insert(
                END,
                f"ID: {r[0]}  |  {r[1]}  |  {r[2]}  |  {r[3]}  |  {r[4]}"
            )

    show()
    win.mainloop()
