from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, exceptions
from models import db, User, Train, Booking
from werkzeug.security import generate_password_hash, check_password_hash

user_blueprint = Blueprint('user_blueprint', __name__)

def handle_jwt_exceptions(error):
    if isinstance(error, exceptions.ExpiredSignatureError):
        return jsonify({"message": "Token has expired. Please log in again."}), 401
    elif isinstance(error, exceptions.InvalidTokenError):
        return jsonify({"message": "Invalid token. Please log in again."}), 401
    return jsonify({"message": "Unknown error occurred."}), 500

@user_blueprint.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400
    
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201

@user_blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    
    return jsonify({"message": "Invalid credentials"}), 401

@user_blueprint.route('/trains/availability', methods=['GET'])
@jwt_required()
def get_seat_availability():
    source = request.args.get('source')
    destination = request.args.get('destination')
    
    trains = Train.query.filter_by(source=source, destination=destination).all()
    availability = []
    
    for train in trains:
        booked_seats = Booking.query.filter_by(train_id=train.id).count()
        available_seats = train.total_seats - booked_seats
        availability.append({
            "train_id": train.id,
            "train_name": train.name,
            "available_seats": available_seats
        })
    
    return jsonify(availability), 200

@user_blueprint.route('/user/bookings', methods=['POST'])
@jwt_required()
def book_seat():
    try:
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        data = request.get_json()
        train_id = data.get('train_id')

        train = Train.query.with_for_update().get(train_id)
        if not train:
            return jsonify({"message": "Train not found"}), 404

        booked_seats = Booking.query.filter_by(train_id=train_id).count()
        
        if booked_seats >= train.total_seats:
            return jsonify({"message": "No seats available"}), 400

        new_booking = Booking(user_id=current_user.id, train_id=train_id, seat_number=booked_seats + 1)
        db.session.add(new_booking)
        db.session.commit()

        return jsonify({"message": "Seat booked successfully", "booking_id": new_booking.id}), 201

    except exceptions.ExpiredSignatureError as e:
        return handle_jwt_exceptions(e)
    except exceptions.InvalidTokenError as e:
        return handle_jwt_exceptions(e)
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Booking failed, please try again"}), 500

@user_blueprint.route('/user/bookings/info', methods=['GET'])
@jwt_required()
def get_user_bookings():
    try:
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        
        bookings = Booking.query.filter_by(user_id=current_user.id).all()
        if not bookings:
            return jsonify({"message": "No bookings found for this user"}), 404
        
        booking_details = []
        for booking in bookings:
            train = Train.query.get(booking.train_id)
            booking_details.append({
                "booking_id": booking.id,
                "train_name": train.name,
                "source": train.source,
                "destination": train.destination,
                "seat_number": booking.seat_number
            })
        
        return jsonify(booking_details), 200

    except exceptions.ExpiredSignatureError as e:
        return handle_jwt_exceptions(e)
    except exceptions.InvalidTokenError as e:
        return handle_jwt_exceptions(e)