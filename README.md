# E-Commerce Management System

A Flask-based e-commerce admin panel for managing products, customers, sales, and inventory.

## Prerequisites

- Python 3.14+
- MySQL (via XAMPP)
- Flask
- MySQL Connector/Python

## Installation

### 1. Install Dependencies

```bash
pip install flask mysql-connector-python
```

### 2. Set Up the Database

- Start XAMPP and ensure MySQL is running.
- Initialize the database:

```bash
python init.py
```

### 3. Run the Application

```bash
python app.py
```

Or, if using your configured Python executable:

```bash
"C:/Users/fathima m/.local/bin/python3.14.exe" app.py
```

### 4. Access the Application

Open your browser and visit:

```
http://localhost:5000
```

Log in using the default credentials:

- **Username:** `admin`
- **Password:** `admin`

## Features

- **Dashboard:** Sales charts and statistics (Dark Mode)
- **Products:** Add, edit, delete, and manage stock
- **Customers:** Full CRUD with email validation
- **Billing:** Multi-item billing with automatic stock deduction
- **Sales:** Complete sales history with details
- **Validation:** Server-side input validation and stock integrity

## Database Schema

- `admin` – Stores administrator credentials
- `products` – Product catalog
- `customers` – Customer information
- `sales` – Sales transactions
- `sale_items` – Individual items in each sale
- `stock` – Product inventory

## Default Login

- **Username:** `admin`
- **Password:** `admin`
