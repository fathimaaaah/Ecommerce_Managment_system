from flask import Flask, render_template, request, redirect, session, flash
from db import connect

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- LOGIN ----------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")

        db = connect()
        cur = db.cursor()

        cur.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (user, pwd)
        )

        result = cur.fetchone()
        print("LOGIN RESULT:", result)  # DEBUG

        if result:
            session["admin"] = user
            return redirect("/dashboard")
        else:
            return "Invalid Login ❌"

    return render_template("login.html")


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect("/")

    db = connect()
    cur = db.cursor()

    # Counts
    cur.execute("SELECT COUNT(*) FROM products")
    products = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM customers")
    customers = cur.fetchone()[0]

    cur.execute("SELECT IFNULL(SUM(total),0) FROM sales")
    revenue = cur.fetchone()[0]

    # Get daily sales data
    cur.execute("SELECT DATE(date) as sale_date, SUM(total) as daily_total FROM sales GROUP BY DATE(date) ORDER BY sale_date")
    daily_sales = cur.fetchall()

    # Get stock data
    cur.execute("SELECT p.name, IFNULL(s.quantity, 0) FROM products p LEFT JOIN stock s ON p.id = s.product_id")
    stock_data = cur.fetchall()

    return render_template(
        "dashboard.html",
        products=products,
        customers=customers,
        revenue=revenue,
        daily_sales=daily_sales,
        stock_data=stock_data
    )


# ---------- PRODUCTS ----------
@app.route("/products")
def products():
    if "admin" not in session:
        return redirect("/")

    db = connect()
    cur = db.cursor()

    cur.execute("SELECT p.id, p.name, p.price, IFNULL(s.quantity, 0) FROM products p LEFT JOIN stock s ON p.id = s.product_id")
    data = cur.fetchall()

    return render_template("products.html", products=data)


@app.route("/add_product", methods=["POST"])
def add_product():
    if "admin" not in session:
        return redirect("/")

    name = request.form["name"]
    price = request.form["price"]

    db = connect()
    cur = db.cursor()

    cur.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
    product_id = cur.lastrowid

    # Add initial stock
    cur.execute("INSERT INTO stock (product_id, quantity) VALUES (%s, %s)", (product_id, 10))

    db.commit()
    return redirect("/products")


@app.route("/delete_product/<int:id>")
def delete_product(id):
    if "admin" not in session:
        return redirect("/")

    db = connect()
    cur = db.cursor()

    # Check if product has been sold (exists in sale_items)
    cur.execute("SELECT COUNT(*) FROM sale_items WHERE product_id = %s", (id,))
    sale_count = cur.fetchone()[0]

    if sale_count > 0:
        db.close()
        flash(f"Cannot delete product - it has been sold {sale_count} time(s). Please remove related sales first.", "danger")
        return redirect("/products")

    # Safe to delete - no sales records
    cur.execute("DELETE FROM stock WHERE product_id=%s", (id,))
    cur.execute("DELETE FROM products WHERE id=%s", (id,))

    db.commit()
    db.close()
    flash("Product deleted successfully!", "success")
    return redirect("/products")


@app.route("/update_stock", methods=["POST"])
def update_stock():
    if "admin" not in session:
        return redirect("/")

    product_id = request.form["product_id"]
    quantity = int(request.form["quantity"])

    db = connect()
    cur = db.cursor()

    # Check if stock entry exists for this product
    cur.execute("SELECT id FROM stock WHERE product_id = %s", (product_id,))
    existing_stock = cur.fetchone()

    if existing_stock:
        # Update existing stock
        cur.execute("UPDATE stock SET quantity = %s WHERE product_id = %s", (quantity, product_id))
    else:
        # Insert new stock entry
        cur.execute("INSERT INTO stock (product_id, quantity) VALUES (%s, %s)", (product_id, quantity))

    db.commit()
    return redirect("/products")


# ---------- CUSTOMERS ----------
@app.route("/customers")
def customers():
    if "admin" not in session:
        return redirect("/")

    db = connect()
    cur = db.cursor()

    cur.execute("SELECT * FROM customers")
    data = cur.fetchall()

    return render_template("customers.html", customers=data)


@app.route("/add_customer", methods=["POST"])
def add_customer():
    if "admin" not in session:
        return redirect("/")

    name = request.form["name"]
    phone = request.form["phone"]
    email = request.form["email"]
    address = request.form["address"]

    db = connect()
    cur = db.cursor()

    cur.execute("""
        INSERT INTO customers(name, phone, email, address)
        VALUES(%s,%s,%s,%s)
    """, (name, phone, email, address))

    db.commit()
    return redirect("/customers")


@app.route("/delete_customer/<int:id>")
def delete_customer(id):
    if "admin" not in session:
        return redirect("/")

    db = connect()
    cur = db.cursor()

    cur.execute("DELETE FROM customers WHERE id=%s", (id,))
    db.commit()

    return redirect("/customers")


# ---------- BILLING ----------
@app.route("/billing")
def billing():
    if "admin" not in session:
        return redirect("/")

    db = connect()
    cur = db.cursor()

    cur.execute("SELECT * FROM products")
    products = cur.fetchall()

    cur.execute("SELECT * FROM customers")
    customers = cur.fetchall()

    return render_template("billing.html",
                           products=products,
                           customers=customers)


# ---------- CREATE SALE ----------
@app.route("/create_sale", methods=["POST"])
def create_sale():
    if "admin" not in session:
        return redirect("/")

    customer_id = request.form.get("customer_id")
    product_ids = request.form.getlist("product_id")
    quantities = request.form.getlist("quantity")

    if not customer_id:
        return "Error: Please select a customer."

    # Filter out empty entries
    items = []
    for i in range(len(product_ids)):
        pid = product_ids[i]
        qty_str = quantities[i]
        if pid and qty_str:
            try:
                qty = int(qty_str)
                if qty > 0:
                    items.append((pid, qty))
            except ValueError:
                continue

    if not items:
        return "Error: Please add at least one valid item."

    db = connect()
    cur = db.cursor()

    # Check stock for all items
    for pid, qty in items:
        cur.execute("SELECT quantity FROM stock WHERE product_id=%s", (pid,))
        stock_row = cur.fetchone()
        if not stock_row or stock_row[0] < qty:
            db.close()
            return f"Error: Insufficient stock for product ID {pid}."

    total = 0

    # calculate total
    for pid, qty in items:
        cur.execute("SELECT price FROM products WHERE id=%s", (pid,))
        price = cur.fetchone()[0]
        total += price * qty

    # insert sale
    cur.execute(
        "INSERT INTO sales(customer_id,total) VALUES(%s,%s)",
        (customer_id, total)
    )

    sale_id = cur.lastrowid

    # insert items + update stock
    for pid, qty in items:
        cur.execute("SELECT price FROM products WHERE id=%s", (pid,))
        price = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO sale_items(sale_id,product_id,quantity,price)
            VALUES(%s,%s,%s,%s)
        """, (sale_id, pid, qty, price))

        # reduce stock
        cur.execute("""
            UPDATE stock
            SET quantity = quantity - %s
            WHERE product_id = %s
        """, (qty, pid))

    db.commit()
    db.close()

    return redirect("/dashboard")


if __name__ == "__main__":
    app.run(debug=True)
