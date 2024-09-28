from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)

class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    source = db.Column(db.String(255), nullable=False)
    destination = db.Column(db.String(255), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    bookings = db.relationship('Booking', backref='train', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    train_id = db.Column(db.Integer, db.ForeignKey('train.id', ondelete='CASCADE'), nullable=False)
    seat_number = db.Column(db.Integer, nullable=False)
