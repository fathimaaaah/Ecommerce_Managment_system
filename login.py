from tkinter import *
from db import connect
from admin import admin_panel


def login_window():

    def login():
        db = connect()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username_entry.get(), password_entry.get())
        )
        if cur.fetchone():
            win.destroy()
            admin_panel()
        else:
            message_label.config(text="Invalid username or password", fg="red")

    # ================= WINDOW =================
    win = Tk()
    win.title("E-Commerce Management System")
    win.geometry("550x450")
    win.configure(bg="#f4f6f9")
    win.resizable(False, False)

    # ================= HEADER =================
    header = Frame(win, bg="#1f2937", height=60)
    header.pack(fill=X)

    Label(
        header,
        text="ADMIN LOGIN",
        bg="#1f2937",
        fg="white",
        font=("Segoe UI", 16, "bold")
    ).pack(pady=15)

    # ================= CARD =================
    card = Frame(win, bg="white", padx=30, pady=25)
    card.pack(pady=30)

    Label(
        card,
        text="Welcome Back",
        bg="white",
        fg="#111827",
        font=("Segoe UI", 14, "bold")
    ).pack(pady=(0, 15))

    # ================= USERNAME =================
    Label(
        card,
        text="Username",
        bg="white",
        fg="#374151",
        anchor="w"
    ).pack(fill=X)

    username_entry = Entry(card, font=("Segoe UI", 11))
    username_entry.pack(fill=X, pady=5)
    username_entry.insert(0, "admin")

    # ================= PASSWORD =================
    Label(
        card,
        text="Password",
        bg="white",
        fg="#374151",
        anchor="w"
    ).pack(fill=X, pady=(10, 0))

    password_entry = Entry(card, font=("Segoe UI", 11), show="*")
    password_entry.pack(fill=X, pady=5)
    password_entry.insert(0, "admin")

    # ================= LOGIN BUTTON =================
    Button(
        card,
        text="LOGIN",
        command=login,
        bg="#2563eb",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        relief=FLAT,
        pady=8
    ).pack(fill=X, pady=15)

    # ================= MESSAGE =================
    message_label = Label(card, text="", bg="white", font=("Segoe UI", 10))
    message_label.pack()

    win.mainloop()
