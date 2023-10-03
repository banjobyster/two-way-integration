import os
import stripe
from dotenv import load_dotenv
from flask import request, jsonify
from db import create_customer, delete_customer_by_email, update_customer_by_email, update_customer_by_stripe_id

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env')
load_dotenv(dotenv_path)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
stripe_signing_key = os.getenv("STRIPE_WEBHOOK_SIGNING_KEY")

def stripe_webhook_endpoints(app_webhook):
    @app_webhook.route('/webhook/stripe', methods=['POST'])
    def handle_customer_added():
        try:
            payload = request.get_json()
            
            # Verify the Stripe webhook signature for security
            sig_header = request.headers.get('Stripe-Signature')
            event = stripe.Webhook.construct_event(
                request.data, sig_header, stripe_signing_key
            )

            stripe_id = event['data']['object']['id']
            email = event['data']['object']['email']
            name = event['data']['object']['name']
            
            # Handle the customer added event
            if event['type'] == 'customer.created':
                try:
                    create_customer(name, email)
                except Exception as e:
                    print("Customer already exists!")
                update_customer_by_email(name, email, stripe_id)
            elif event['type'] == 'customer.deleted':
                delete_customer_by_email(email)
            elif event['type'] == 'customer.updated':
                update_customer_by_stripe_id(name, email, stripe_id)

            return jsonify({'status': 'success'})
        except Exception as e:
            return jsonify({'status': 'error', 'error_message': str(e)}), 400

    # Endpoint for checking Stripe webhook status
    @app_webhook.route('/webhook/stripe', methods=['GET'])
    def stripe_webhook_status():
        return jsonify({'message': 'Stripe Webhook Active'})