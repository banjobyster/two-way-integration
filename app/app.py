from flask import Flask
from apis import configure_apis
from db import init_db, close_db
from workers.kafka_workers import kafka_event_consumer
from multiprocessing import Process

# Initializing Flask app
app = Flask(__name__)

# CRUD API routes
configure_apis(app)

# Initializing kafka to stripe worker
kafka_consumer_process = Process(target=kafka_event_consumer)

# Running app
if __name__ == "__main__":
    init_db()
    kafka_consumer_process.start()  

    app.run(debug=False,host='0.0.0.0')

    close_db()
    kafka_consumer_process.join()