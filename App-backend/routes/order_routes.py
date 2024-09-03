from flask import Blueprint, request, jsonify
from app import db
from models.order import Order
from models.restaurant import Restaurant
from flask_jwt_extended import jwt_required, get_jwt_identity

order_routes = Blueprint('order_routes', __name__)

@order_routes.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    current_user = get_jwt_identity()
    orders = Order.query.filter_by(customer_id=current_user['id']).all()
    return jsonify([{
        'id': o.id,
        'restaurant_id': o.restaurant_id,
        'items': o.items,
        'total_price': o.total_price,
        'status': o.status
    } for o in orders]), 200

@order_routes.route('/order', methods=['POST'])
@jwt_required()
def place_order():
    current_user = get_jwt_identity()
    data = request.get_json()
    
    restaurant = Restaurant.query.get_or_404(data['restaurant_id'])
    
    new_order = Order(
        customer_id=current_user['id'],
        restaurant_id=restaurant.id,
        items=data['items'],
        total_price=data['total_price'],
        status='Pending'
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order placed successfully!'}), 201

@order_routes.route('/order/<int:id>', methods=['GET'])
@jwt_required()
def get_order(id):
    current_user = get_jwt_identity()
    order = Order.query.get_or_404(id)
    if order.customer_id != current_user['id']:
        return jsonify({'message': 'Access denied'}), 403

    return jsonify({
        'id': order.id,
        'restaurant_id': order.restaurant_id,
        'items': order.items,
        'total_price': order.total_price,
        'status': order.status
    }), 200

@order_routes.route('/order/<int:id>', methods=['PUT'])
@jwt_required()
def update_order(id):
    current_user = get_jwt_identity()
    order = Order.query.get_or_404(id)
    if order.customer_id != current_user['id']:
        return jsonify({'message': 'Access denied'}), 403

    data = request.get_json()
    order.status = data.get('status', order.status)
    db.session.commit()
    return jsonify({'message': 'Order updated successfully!'}), 200

@order_routes.route('/order/<int:id>', methods=['DELETE'])
@jwt_required()
def cancel_order(id):
    current_user = get_jwt_identity()
    order = Order.query.get_or_404(id)
    if order.customer_id != current_user['id']:
        return jsonify({'message': 'Access denied'}), 403

    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order cancelled successfully!'}), 200
