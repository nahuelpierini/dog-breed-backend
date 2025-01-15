from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.entities.user import User
from src.models.user_model import UserModel
import uuid
from datetime import timedelta

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    """
    Handles user login by verifying the provided email and password. 

    If the credentials are valid, a JWT access token is generated with a 24-hour expiration.

    Returns:
        jsonify: A JSON response with the success status and the generated JWT token on successful login, or an error message on failure.
    """
    try:
        email: str = request.form['email']
        upassword: str = request.form['password']
        user: User = UserModel.login(User(0, email, upassword))
        
        if user and user.upassword:
            access_token: str = create_access_token(identity=user.userid, expires_delta=timedelta(hours=24))
            return jsonify({
                "success": True,
                "access_token": access_token,
                "message": "Login successful"
            }), 200
        else:
            return jsonify({"success": False, "message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@auth.route('/register', methods=['POST'])
def register():
    """
    Handles the registration of a new user by accepting necessary details 
    from the request and registering the user in the database.

    If the email is already registered, an error message is returned. 

    Returns:
        jsonify: A JSON response with success status and message, or an error message if registration fails.
    """
    if request.method == 'POST':
        email: str = request.form['email']
        upassword: str = request.form['password']
        firstname: str = request.form['first_name']
        lastname: str = request.form['last_name']
        birthdate: str = request.form['birth_date']
        country: str = request.form['country']
        userid: str = str(uuid.uuid4())
        
        new_user: User = User(userid, email, upassword, firstname, lastname, birthdate, country)
        
        try:
            UserModel.register(new_user)
            return jsonify({"success": True, "message": "User registered successfully"}), 201
        except Exception as e:
            if 'Email already registered' in str(e):
                return jsonify({"success": False, "message": "Email already registered"}), 400
            return jsonify({"success": False, "error": str(e)}), 500
    else:
        return jsonify({"success": False, "message": "Invalid request method"}), 405
