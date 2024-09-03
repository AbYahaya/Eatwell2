from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)

# Load configuration from config.py
app.config.from_object('config.Config')

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

# Import and register blueprints for routes
from routes.user_routes import user_routes
from routes.restaurant_routes import restaurant_routes
from routes.order_routes import order_routes

app.register_blueprint(user_routes)
app.register_blueprint(restaurant_routes)
app.register_blueprint(order_routes)

if __name__ == '__main__':
    app.run(debug=True)
