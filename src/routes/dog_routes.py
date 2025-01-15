from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid
from src.models.dog_model import DogModel
from src.services.azure_storage_connection import AzureBlobStorage
from src.models.entities.dogs import Dog

dog_bp = Blueprint('dog_bp', __name__)

blob_storage_instance = None

def get_blob_storage():
    """
    It is a Singleton pattern.
    Retrieves the Azure Blob Storage instance. If it hasn't been created yet, it initializes it with the connection string and container name 
    from the app's configuration.

    Returns:
        AzureBlobStorage: The singleton instance of the AzureBlobStorage class for handling file uploads.
    """
    config = current_app.config
    AZURE_STORAGE_CONNECTION_STRING = config('AZURE_STORAGE_CONNECTION_STRING')
    CONTAINER_NAME = config('CONTAINER_NAME')

    global blob_storage_instance
    if blob_storage_instance is None:
        blob_storage_instance = AzureBlobStorage(AZURE_STORAGE_CONNECTION_STRING)
    return blob_storage_instance

@dog_bp.route('/upload_dog', methods=['POST'])
@jwt_required()
def upload_dog():
    """
    Uploads a new dog or updates an existing dog's information. If a dog already exists for the current user, it updates the dogs details.
    Optionally uploads a new image to Azure Blob Storage.

    Returns:
        jsonify: A JSON response indicating the success or failure of the operation.
    """
    try:
        userid = get_jwt_identity()
        existing_dog = DogModel.get_dog_by_user(userid)
        
        breed = request.form['breed']
        dogname = request.form['name']
        age = request.form['age']
        
        image = request.files.get('image')

        if existing_dog:
            existing_dog.dogname = dogname
            existing_dog.breed = breed
            existing_dog.age = age
            
            if image:
                existing_dog.imageurl = blob_storage_instance.upload_file(image, breed)
            
            DogModel.update_dog(existing_dog)
            return jsonify({"success": True, "message": "Dog updated successfully!"})

        else:
            imageurl = ''
            if image:
                imageurl = blob_storage_instance.upload_file(image, breed)
            dogid = str(uuid.uuid4())
            dog = Dog(dogid, dogname, breed, age, userid, imageurl)
            DogModel.save_dog(dog)
            return jsonify({"success": True, "message": "Dog uploaded successfully!"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@dog_bp.route('/edit_dog/<dogid>', methods=['PUT'])
@jwt_required()
def edit_dog(dogid):
    """
    Edits the details of an existing dog. The dog must belong to the current user. 
    This route updates the dog's name, breed, and age.

    Args:
        dogid (str): The ID of the dog to be updated.

    Returns:
        jsonify: A JSON response indicating the success or failure of the operation.
    """
    try:
        userid = get_jwt_identity()

        dog = DogModel.get_dog_by_id(dogid)
        if dog is None:
            return jsonify({"success": False, "message": "Dog not found"}), 404
        
        if dog.userid != userid:
            return jsonify({"success": False, "message": "Unauthorized access"}), 403

        dogname = request.form['name']
        breed = request.form['breed']
        age = request.form['age']

        if not dogname or not breed or not age:
            return jsonify({"success": False, "message": "Missing data"}), 400

        dog.dogname = dogname
        dog.breed = breed
        dog.age = age
        DogModel.update_dog(dog)

        return jsonify({"success": True, "message": "Dog updated successfully!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@dog_bp.route('/get_dog', methods=['GET'])
@jwt_required()
def get_dog():
    """
    Retrieves all dogs associated with the current user. If no dogs are found, an empty list is returned.

    Returns:
        jsonify: A JSON response with the list of dogs or an empty list if no dogs are found.
    """
    try:
        userid = get_jwt_identity()
        
        dogs = DogModel.get_dogs_by_user_id(userid)
        
        if not dogs:
            return jsonify({"success": True, "data": []}), 200

        dogs_data = []
        for dog in dogs:
            dogs_data.append({
                "id": dog.dogid,
                "name": dog.dogname,
                "breed": dog.breed,
                "age": dog.age,
                "image_url": dog.imageurl
            })
        
        return jsonify({
            "success": True,
            "data": dogs_data
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@dog_bp.route('/upload_dog_image/<dogid>', methods=['POST'])
@jwt_required()
def upload_dog_image(dogid):
    """
    Uploads a new image for an existing dog. The dog must belong to the current user. 

    Args:
        dogid (str): The ID of the dog whose image is being updated.

    Returns:
        jsonify: A JSON response indicating the success or failure of the operation.
    """
    try:
        userid = get_jwt_identity()

        dog = DogModel.get_dog_by_id(dogid)
        if dog is None:
            return jsonify({"success": False, "message": "Dog not found"}), 404

        if dog.userid != userid:
            return jsonify({"success": False, "message": "Unauthorized access"}), 403

        image = request.files.get('image')
        if not image:
            return jsonify({"success": False, "message": "No image provided"}), 400

        imageurl = blob_storage_instance.upload_file(image, dog.breed)

        dog.imageurl = imageurl
        DogModel.update_dog(dog)

        return jsonify({"success": True, "message": "Dog image updated successfully!"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
