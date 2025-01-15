from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user_model import UserModel

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Retrieves the current user's profile data. The user must be authenticated via JWT.

    Returns:
        jsonify: A JSON response containing the user's profile data or null if no user is found.
    """
    try:
        userid = get_jwt_identity()
        user = UserModel.get_by_id(userid)
        
        if not user:
            return jsonify({"success": True, "data": None}), 200

        user_data = {
            "user_id": user.userid,
            "email": user.email,
            "first_name": user.firstname,
            "last_name": user.lastname,
            "birth_date": user.birthdate,
            "country": user.country
        }

        return jsonify({"success": True, "data": user_data})
    except Exception as e:
        print("Error in get_profile:", e) 
        return jsonify({"success": False, "error": str(e)}), 500


@profile_bp.route('/profile/edit', methods=['PUT'])
@jwt_required()
def edit_profile():
    """
    Edits the current user's profile data. The user must be authenticated via JWT. 
    Allows updating first name, last name, birth date, and country.

    Returns:
        jsonify: A JSON response indicating the success or failure of the profile update.
    """
    try:
        userid = get_jwt_identity()
        user = UserModel.get_by_id(userid)
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        data = request.form 

        user.firstname = data.get('first_name', user.firstname)
        user.lastname = data.get('last_name', user.lastname)
        user.birthdate = data.get('birth_date', user.birthdate)
        user.country = data.get('country', user.country)

        UserModel.update_user(user)

        return jsonify({"success": True, "message": "User profile updated successfully"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
