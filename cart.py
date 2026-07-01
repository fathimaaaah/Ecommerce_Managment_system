from tkinter import *
from db import connect

def cart_window(uid):
    win = Tk()
    win.title("My Cart")
    win.geometry("500x400")

    listbox = Listbox(win,width=60)
    listbox.pack()

    def load():
        listbox.delete(0,END)
        db=connect()
        cur=db.cursor()
        cur.execute("""
        SELECT cart.id,products.name,cart.quantity,products.price 
        FROM cart JOIN products ON cart.product_id=products.id 
        WHERE user_id=%s
        """,(uid,))
        for c in cur.fetchall():
            listbox.insert(END,c)

    cid = Entry(win)
    cid.pack()
    cid.insert(0,"Cart ID")

    qty = Entry(win)
    qty.pack()
    qty.insert(0,"New Quantity")

    def update():
        db=connect()
        cur=db.cursor()
        cur.execute("UPDATE cart SET quantity=%s WHERE id=%s",(qty.get(),cid.get()))
        db.commit()
        load()

    def delete():
        db=connect()
        cur=db.cursor()
        cur.execute("DELETE FROM cart WHERE id=%s",(cid.get(),))
        db.commit()
        load()

    Button(win,text="Update Qty",command=update).pack()
    Button(win,text="Remove Item",command=delete).pack()

    load()
    win.mainloop()
