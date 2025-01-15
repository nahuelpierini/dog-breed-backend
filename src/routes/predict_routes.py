from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from PIL import Image
import io
import numpy as np
import requests
import base64
import json
from src.models.prediction_models import get_model
from src.services.preprocess_model import preprocess_image
from src.utils.label_mapping import get_label_mapping
from src.services.azure_storage_connection import AzureBlobStorage

predict_bp = Blueprint('predict', __name__)

def predict_local(file):
    model = get_model()
    label_mapping = get_label_mapping()

    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    img = Image.open(io.BytesIO(file.read()))
    img_array = preprocess_image(img)

    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions[0])
    predicted_label = label_mapping[str(predicted_class)]
    confidence = round((predictions[0][predicted_class]) * 100, 2)

    return predicted_label, confidence


def predict_azure(file, config):
    url = config['AZURE_ML_URL']
    aml_token = config['AZURE_ML_TOKEN']

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {aml_token}"
    }

    img = file.read()
    image_base64 = base64.b64encode(img).decode('utf-8')

    json_payload = {
        "data": image_base64
    }

    response = requests.post(url, json=json_payload, headers=headers)
    prediction = json.loads(response.json())
    predicted_label = prediction.get('breed')
    confidence = prediction.get('confidence')

    return predicted_label, confidence


@predict_bp.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    """
    Handles POST requests to the '/predict' endpoint.
    Predicts the breed of the dog based on the uploaded image file.
    If the prediction confidence is greater than 95%, uploads the image to Blob Storage.
    """
    config = current_app.config
    userid = get_jwt_identity()

    file = request.files['file']

    if current_app.config['DEBUG']:
        predicted_label, confidence = predict_local(file)
        print("DEV")
    else:
        predicted_label, confidence = predict_azure(file, config)
        print("PROD")


    if confidence > 95:
        try:

            connection_string = config['AZURE_STORAGE_CONNECTION_STRING']
            container_name = config['CONTAINER_NAME']
            azure_blob_storage = AzureBlobStorage(connection_string)

            file.seek(0)
            content_type = file.content_type
            print("\n")
            print("CONTENT TYPE: ")
            print(content_type)
            print("\n")

            azure_blob_storage.upload_image(
                container_name=container_name,
                folder_name=predicted_label,
                file_data=file,
                blob_name=predicted_label,
                content_type=content_type
            )
        except Exception as e:
            return jsonify({
                'breed': predicted_label,
                'confidence': confidence,
                'message': f"Prediction succeeded, but failed to upload image: {str(e)}"
            }), 500

    return jsonify({
        'breed': predicted_label,
        'confidence': confidence
    })
