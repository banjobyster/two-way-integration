import mysql.connector
from config import db_config

# database global connection and cursor
conn = None
cursor = None

# initializing database connection
def init_db():
    global conn, cursor
    try:
        # Connect to the MySQL server
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Create the 'zenskar' database if it doesn't exist
        create_db_query = "CREATE DATABASE IF NOT EXISTS zenskar"
        cursor.execute(create_db_query)

        # Switch to the 'zenskar' database
        conn.database = "zenskar"

        # Create the 'customer' table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS customer (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE
        )
        """
        cursor.execute(create_table_query)
        conn.commit()
    except Exception as e:
        print(f"Error: {str(e)}")

# CRUD functions
def create_customer(name, email):
    try:
        query = "INSERT INTO customer (name, email) VALUES (%s, %s)"
        values = (name, email)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        print(f"Error creating customer: {str(e)}")
        raise Exception("Internal Server Error")

def read_customer(customer_id):
    try:
        print(customer_id, cursor)
        query = "SELECT * FROM customer WHERE id = %s"
        cursor.execute(query, (customer_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error reading customer: {str(e)}")
        raise Exception("Internal Server Error")

def update_customer(customer_id, name, email):
    try:
        query = "UPDATE customer SET name = %s, email = %s WHERE id = %s"
        values = (name, email, customer_id)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        print(f"Error updating customer: {str(e)}")
        raise Exception("Internal Server Error")

def delete_customer(customer_id):
    try:
        query = "DELETE FROM customer WHERE id = %s"
        cursor.execute(query, (customer_id,))
        conn.commit()
    except Exception as e:
        print(f"Error deleting customer: {str(e)}")
        raise Exception("Internal Server Error")

# Get all customers
def get_all_customers():
    try:
        query = "SELECT * FROM customer"
        cursor.execute(query)
        customers = cursor.fetchall()

        customer_list = [{"id": row[0], "name": row[1], "email": row[2]} for row in customers]

        return customer_list
    except Exception as e:
        print(f"Error fetching customers: {str(e)}")
        raise Exception("Internal Server Error")

# closing database connection when app closes
def close_db():
    try:
        print("Database closed")
        conn.close()
    except Exception as e:
        print(f"Error closing database connection: {str(e)}")