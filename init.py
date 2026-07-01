import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ecommerce_db"
    )

# Create database if not exists
def create_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    cur = conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS ecommerce_db")
    conn.commit()
    conn.close()

# Create tables
def create_tables():
    db = connect()
    cur = db.cursor()

    # Admin table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admin (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            password VARCHAR(50)
        )
    """)

    # Products table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            price DECIMAL(10,2)
        )
    """)

    # Customers table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20),
            email VARCHAR(100),
            address TEXT
        )
    """)

    # Sales table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            total DECIMAL(10,2),
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)

    # Add date column if it doesn't exist (for existing tables)
    try:
        cur.execute("ALTER TABLE sales ADD COLUMN date TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    except mysql.connector.Error as err:
        if err.errno != 1060:  # 1060 is duplicate column
            raise

    # Sale items table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sale_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sale_id INT,
            product_id INT,
            quantity INT,
            price DECIMAL(10,2),
            FOREIGN KEY (sale_id) REFERENCES sales(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    # Stock table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stock (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT UNIQUE,
            quantity INT,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    # Clean up duplicate stock entries (keep the one with highest id)
    cur.execute("""
        DELETE s1 FROM stock s1
        INNER JOIN stock s2
        WHERE s1.id < s2.id AND s1.product_id = s2.product_id
    """)

    # Add unique constraint to existing stock table if it doesn't exist
    try:
        cur.execute("ALTER TABLE stock ADD UNIQUE (product_id)")
    except mysql.connector.Error as err:
        if err.errno != 1061:  # 1061 is duplicate key
            raise

    db.commit()
    db.close()

# Insert sample data
def insert_sample_data():
    db = connect()
    cur = db.cursor()

    # Insert admin
    try:
        cur.execute("INSERT INTO admin (username, password) VALUES (%s, %s)", ("admin", "admin"))
    except mysql.connector.IntegrityError:
        pass  # Already exists

    # Insert sample products
    products = [
        ("Laptop", 50000.00),
        ("Mouse", 500.00),
        ("Keyboard", 1500.00),
        ("Monitor", 10000.00)
    ]

    for product in products:
        try:
            cur.execute("INSERT INTO products (name, price) VALUES (%s, %s)", product)
            product_id = cur.lastrowid
            cur.execute("INSERT INTO stock (product_id, quantity) VALUES (%s, %s)", (product_id, 10))
        except mysql.connector.IntegrityError:
            pass

    db.commit()
    db.close()

if __name__ == "__main__":
    create_database()
    create_tables()
    insert_sample_data()
    print("Database initialized successfully!")