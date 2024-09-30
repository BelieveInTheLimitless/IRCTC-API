# IRCTC API

A Flask-based API that allows users to register, login & book train tickets along with API key-based authentication for admins.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)

## Features
- Admin privileges - Add, Update, Delete train/s
- User privileges -  Register, Login, Check Seat Availability, Book Seat/s, Check Booking info
- Optimized for handling race conditions by holding a lock for ongoing transaction
- Admin API endpoints are secured by API Key which are known to Admin and Host
- JWT-based authentication token system for user login with 1 hour expiration window

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

## API Endpoints

### Admin API Endpoints

- **Add Train**  
  `POST /admin/add_train`
  - **Request Headers**  
    `ADMIN-API-KEY: <API_KEY>`
  - **Request Body**  
    ```json
    {
      "name": "Express Train",
      "source": "Pune",
      "destination": "Thane",
      "total_seats": 100
    }
    ```
  - **Response**  
    ```json
    {
      "message": "Train added successfully"
      "train_id": 1
    }
    ```

- **Update Train**  
  `PUT /admin/update_train/<train_id>`
  - **Request Headers**  
    `ADMIN-API-KEY: <API_KEY>`
  - **Request Body**  
    ```json
    {
      "name": "New Express Train",
      "source": "Mumbai",
      "destination": "Delhi",
      "total_seats": 200
    }
    ```
  - **Response**  
    ```json
    {
      "message": "Train updated successfully"
    }
    ```
    
- **Delete Train**  
  `DELETE /admin/delete_train/<train_id>`
  - **Request Headers**  
    `ADMIN-API-KEY: <API_KEY>`
  - **Response**  
    ```json
    {
      "message": "Train deleted successfully"
    }
    ```
  - **Error Response** (if train not found)  
    ```json
    {
      "message": "Train not found"
    }
    ```

### User API Endpoints

- **Register User**  
  `POST /register`
  - **Request Body**  
    ```json
    {
      "username": "john_doe",
      "password": "securepassword"
    }
    ```
  - **Response**  
    ```json
    {
      "message": "User registered successfully"
    }
    ```

- **Login User**  
  `POST /login`
  - **Request Body**  
    ```json
    {
      "username": "john_doe",
      "password": "securepassword"
    }
    ```
  - **Response**  
    ```json
    {
      "access_token": "<JWT_TOKEN>"
    }
    ```

- **Check Seat Availability**  
  `GET /trains/availability`
  - **Request Headers**  
    `Authorization: Bearer <JWT_TOKEN>`
  - **Request Params**  
    - `source`: "Pune"  
    - `destination`: "Thane"
  - **Response**  
    ```json
    [
      {
        "train_id": 1,
        "train_name": "Express Train",
        "available_seats": 50
      }
    ]
    ```

- **Book Seat**  
  `POST /user/bookings`
  - **Request Headers**  
    `Authorization: Bearer <JWT_TOKEN>`
  - **Request Body**  
    ```json
    {
      "train_id": 1
    }
    ```
  - **Response**  
    ```json
    {
      "message": "Seat booked successfully",
      "booking_id": 101
    }
    ```

- **Get User Bookings**  
  `GET /user/bookings/info`
  - **Request Headers**  
    `Authorization: Bearer <JWT_TOKEN>`
  - **Response**  
    ```json
    [
      {
        "booking_id": 101,
        "train_name": "Express Train",
        "source": "Pune",
        "destination": "Thane",
        "seat_number": 50
      }
    ]
    ```


