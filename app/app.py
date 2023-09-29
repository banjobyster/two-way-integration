from flask import Flask
from apis import configure_apis
from db import init_db, close_db

# Initializing Flask app
app = Flask(__name__)

# CRUD API routes
configure_apis(app)

# Running app
if __name__ == "__main__":
    init_db()
    app.run(debug=True,host='0.0.0.0')
    close_db()


