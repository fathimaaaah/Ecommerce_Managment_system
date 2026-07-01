from tkinter import *
from db import connect

def dashboard(uid, role):
    shop = Tk()
    shop.title("E-Commerce Store")
    shop.geometry("600x500")
    shop.configure(bg="white")

    Label(shop, text="Online Shopping Store", font=("Arial",20)).pack(pady=10)

    db = connect()
    cur = db.cursor()
    cur.execute("SELECT * FROM products")

    for p in cur.fetchall():
        Label(shop, text=f"{p[1]}   ₹{p[2]}   Stock:{p[3]}", font=("Arial",12)).pack()
        Button(shop, text="Add to Cart", bg="blue", fg="white").pack(pady=5)

    shop.mainloop()
def add_to_cart(pid,uid):
    db=connect()
    cur=db.cursor()
    cur.execute("INSERT INTO cart(user_id,product_id,quantity) VALUES(%s,%s,1)",(uid,pid))
    db.commit()
