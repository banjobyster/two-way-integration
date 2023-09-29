import mysql.connector
import os
from dotenv import load_dotenv

# Specify the full path to the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')

# Load environment variables from the .env file
load_dotenv(dotenv_path)

# database configuration
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root_password"),
    "port": os.getenv("DB_PORT", "3306"),
}

# database global connection and cursor
conn = None
cursor = None

# initializing database connection
def init_db():
    global conn, cursor
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        create_db_query = "CREATE DATABASE IF NOT EXISTS zenskar"
        cursor.execute(create_db_query)
        conn.database = "zenskar"

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
def read_customer(customer_id):
    try:
        query = "SELECT * FROM customer WHERE id = %s"
        cursor.execute(query, (customer_id,))
        customer_data = cursor.fetchone()
        
        return customer_data
    except Exception as e:
        print(f"Error reading customer: {str(e)}")
        raise Exception("Internal Server Error")
    
def create_customer(name, email):
    try:
        query = "INSERT INTO customer (name, email) VALUES (%s, %s)"
        values = (name, email)
        cursor.execute(query, values)
        conn.commit()

        customer_message = {
            "name": name,
            "email": email,
            "action": "create",
        }
        
        return customer_message
    except Exception as e:
        print(f"Error creating customer: {str(e)}")
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
        customer_data = read_customer(customer_id)

        if customer_data is None:
            raise Exception("Customer not present")

        query = "DELETE FROM customer WHERE id = %s"
        cursor.execute(query, (customer_id,))
        conn.commit()

        name = customer_data[1]
        email = customer_data[2]

        customer_message = {
            "id": customer_id,
            "action": "delete",
            "email": email,
            "name": name,
        }
        
        return customer_message
    except Exception as e:
        print(f"Error deleting customer: {str(e)}")
        raise Exception("Internal Server Error")

def delete_customer_by_email(email):
    try:
        query = "DELETE FROM customer WHERE email = %s"
        cursor.execute(query, (email,))
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
        conn.close()
    except Exception as e:
        print(f"Error closing database connection: {str(e)}")