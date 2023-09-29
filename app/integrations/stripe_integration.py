import os
import stripe
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_customer_stripe(email, name):
    try:
        customer = stripe.Customer.create(
            email=email,
            name=name
        )

        print(f"Customer created for email: {email}")
        return customer
    except stripe.error.StripeError as e:
        print(f"Error creating customer: {e}")
        return None

def delete_customer_stripe(email):
    try:
        customers = stripe.Customer.list(email=email)

        for customer in customers:
            customer.delete()
            print(f"Customer deleted for email: {email}")
            return True

        print(f"No customer found with email: {email}")
        return False
    except stripe.error.StripeError as e:
        print(f"Error deleting customer: {e}")
        return False