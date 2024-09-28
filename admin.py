from flask import Blueprint, request, jsonify, current_app, abort
from functools import wraps
from models import db, Train

admin_blueprint = Blueprint('admin_blueprint', __name__)

def admin_api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('ADMIN-API-KEY')
        if api_key and api_key == current_app.config['ADMIN_API_KEY']:
            return f(*args, **kwargs)
        return jsonify({"message": "Invalid or missing API key"}), 403
    return decorated

def validate_train_data(data):
    required_fields = ['name', 'source', 'destination', 'total_seats']
    for field in required_fields:
        if field not in data:
            abort(400, description=f"Missing field: {field}")
    if not isinstance(data['total_seats'], int) or data['total_seats'] < 0:
        abort(400, description="Total seats must be a non-negative integer.")

@admin_blueprint.route('/admin/add_train', methods=['POST'])
@admin_api_key_required
def add_train():
    data = request.get_json()
    validate_train_data(data)
    new_train = Train(
        name=data['name'],
        source=data['source'],
        destination=data['destination'],
        total_seats=data['total_seats']
    )
    db.session.add(new_train)
    db.session.commit()
    
    return jsonify({
        "message": "Train added successfully",
        "train_id": new_train.id
    }), 201

@admin_blueprint.route('/admin/update_train/<int:train_id>', methods=['PUT'])
@admin_api_key_required
def update_train(train_id):
    train = Train.query.get(train_id)
    if not train:
        return jsonify({"message": "Train not found"}), 404
    
    data = request.get_json()
    train.name = data.get('name', train.name)
    train.source = data.get('source', train.source)
    train.destination = data.get('destination', train.destination)
    train.total_seats = data.get('total_seats', train.total_seats)
    
    db.session.commit()
    return jsonify({"message": "Train updated successfully"}), 200

@admin_blueprint.route('/admin/delete_train/<int:train_id>', methods=['DELETE'])
@admin_api_key_required
def delete_train(train_id):
    train = Train.query.get(train_id)
    if not train:
        return jsonify({"message": "Train not found"}), 404
    
    db.session.delete(train)
    db.session.commit()
    return jsonify({"message": "Train deleted successfully"}), 200