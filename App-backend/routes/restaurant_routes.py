from flask import Blueprint, request, jsonify
from app import db
from models.restaurant import Restaurant
from flask_jwt_extended import jwt_required, get_jwt_identity

restaurant_routes = Blueprint('restaurant_routes', __name__)

@restaurant_routes.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'address': r.address,
        'cuisine_type': r.cuisine_type,
        'owner_id': r.owner_id
    } for r in restaurants]), 200

@restaurant_routes.route('/restaurant/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get_or_404(id)
    return jsonify({
        'id': restaurant.id,
        'name': restaurant.name,
        'address': restaurant.address,
        'cuisine_type': restaurant.cuisine_type,
        'owner_id': restaurant.owner_id
    }), 200

@restaurant_routes.route('/restaurant', methods=['POST'])
@jwt_required()
def add_restaurant():
    current_user = get_jwt_identity()
    if current_user['role'] != 'owner':
        return jsonify({'message': 'Access denied'}), 403

    data = request.get_json()
    new_restaurant = Restaurant(
        name=data['name'],
        address=data['address'],
        cuisine_type=data.get('cuisine_type'),
        owner_id=current_user['id']
    )
    db.session.add(new_restaurant)
    db.session.commit()
    return jsonify({'message': 'Restaurant added successfully!'}), 201

@restaurant_routes.route('/restaurant/<int:id>', methods=['PUT'])
@jwt_required()
def update_restaurant(id):
    current_user = get_jwt_identity()
    restaurant = Restaurant.query.get_or_404(id)
    if restaurant.owner_id != current_user['id']:
        return jsonify({'message': 'Access denied'}), 403

    data = request.get_json()
    restaurant.name = data.get('name', restaurant.name)
    restaurant.address = data.get('address', restaurant.address)
    restaurant.cuisine_type = data.get('cuisine_type', restaurant.cuisine_type)
    db.session.commit()
    return jsonify({'message': 'Restaurant updated successfully!'}), 200

@restaurant_routes.route('/restaurant/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_restaurant(id):
    current_user = get_jwt_identity()
    restaurant = Restaurant.query.get_or_404(id)
    if restaurant.owner_id != current_user['id']:
        return jsonify({'message': 'Access denied'}), 403

    db.session.delete(restaurant)
    db.session.commit()
    return jsonify({'message': 'Restaurant deleted successfully!'}), 200
