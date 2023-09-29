from flask import Flask
from apis import configure_apis
from db import init_db, close_db
from workers.kafka_workers import kafka_event_consumer
from multiprocessing import Process
from integrations.stripe.stripe_webhooks import stripe_webhook_endpoints
import os
from dotenv import load_dotenv
import ssl
from pyngrok import ngrok, conf, installer

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

# Initializing Flask app
app = Flask(__name__)

# CRUD API routes
configure_apis(app)

# Webhook API routes for stripe
stripe_webhook_endpoints(app)

# Running app
if __name__ == "__main__":
    init_db()

    kafka_consumer_process = Process(target=kafka_event_consumer)
    kafka_consumer_process.start()  

    # Ngrok setup for tunneling local server to internet
    pyngrok_config = conf.get_default()
    if not os.path.exists(pyngrok_config.ngrok_path):
        myssl = ssl.create_default_context()
        myssl.check_hostname=False
        myssl.verify_mode=ssl.CERT_NONE
        installer.install_ngrok(pyngrok_config.ngrok_path, context=myssl)

    ngrok.set_auth_token(os.getenv("NGROK_SECRET_KEY", "secret-key"))  
    ngrok_tunnel = ngrok.connect("5000")

    app.run()

    close_db()
    kafka_consumer_process.join()