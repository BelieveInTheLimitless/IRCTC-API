# IRCTC API

A Flask-based API for managing train bookings, user registrations, and admin priviledges like adding or updating trains.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)

## Features
- User registration and login
- JWT-based authentication
- Train management (add, update, view trains)
- Seat availability check
- Booking management

## Technologies Used
- Python3 (Prerequisite)
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- MySQL (Prerequisite)
- dotenv for environment variable management

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/BelieveInTheLimitless/IRCTC-API
cd IRCTC-API
```

### 2. Creating the Database
```bash
#Login to the database
mysql -u root -p
#Create database
CREATE DATABASE railway_db;
#Create user
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
#Grant privileges
GRANT ALL PRIVILEGES ON railway_db.* TO 'user'@'localhost';
#Update privileges
FLUSH PRIVILEGES;
#Exit
EXIT;
```

### 3. Creating a virtual environment
```bash
# Common
python3 -m venv .venv
# For Linux
source .venv/bin/activate
# For Windows
.venv\Scripts\activate
```

### 4. Installing the required packages
```bash
pip3 install -r requirements.txt
```

### 5. Running the application
```bash
python3 app.py
```
