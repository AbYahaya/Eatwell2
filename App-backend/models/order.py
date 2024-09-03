from app import db

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    items = db.Column(db.String(200), nullable=False)  # For simplicity; use JSON or a related table in production
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # e.g., 'Pending', 'Completed', 'Cancelled'

    def __repr__(self):
        return f'<Order {self.id} by {self.customer_id}>'