from flask import Flask
from apis import configure_api_routes
from db import init_db, close_db

# Initializing Flask app
app = Flask(__name__)

# CRUD API routes
configure_api_routes(app)

# Running app
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
    close_db()


