from flask import jsonify, request
from db import create_customer, read_customer, update_customer, delete_customer, get_all_customers

# api routes configuration
def configure_apis(app):
    #post route to add new customer
    @app.route("/customer", methods=["POST"])
    def add_customer():
        try:
            data = request.get_json()
            name = data["name"]
            email = data["email"]
            create_customer(name, email)
            return jsonify({"message": "Customer added successfully"})
        except Exception as e:
            return jsonify({"error": f"Failed to add customer: {str(e)}"}), 500

    #get route to get customer by id
    @app.route("/customer/<int:customer_id>", methods=["GET"])
    def get_customer(customer_id):
        try:
            customer = read_customer(customer_id)
            if customer:
                return jsonify({"customer": customer})
            else:
                return jsonify({"message": "Customer not found"}), 404
        except Exception as e:
            return jsonify({"error": f"Failed to retrieve customer: {str(e)}"}), 500

    #put route to update existing customer
    @app.route("/customer/<int:customer_id>", methods=["PUT"])
    def update_customer_info(customer_id):
        try:
            data = request.get_json()
            name = data["name"]
            email = data["email"]
            update_customer(customer_id, name, email)
            return jsonify({"message": "Customer updated successfully"})
        except Exception as e:
            return jsonify({"message": f"Error updating customer: {str(e)}"}), 500

    #delete route to remove existing customer
    @app.route("/customer/<int:customer_id>", methods=["DELETE"])
    def remove_customer(customer_id):
        try:
            delete_customer(customer_id)
            return jsonify({"message": "Customer deleted successfully"})
        except Exception as e:
            return jsonify({"message": f"Error deleting customer: {str(e)}"}), 500

    #get route to get all customers
    @app.route("/customers", methods=["GET"])
    def get_all_customers_route():
        try:
            customers = get_all_customers()
            return jsonify({"customers": customers})
        except Exception as e:
            return jsonify({"message": f"Error fetching customers: {str(e)}"}), 500