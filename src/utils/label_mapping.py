from flask import current_app
import json
from urllib.parse import urlparse
from src.services.azure_storage_connection import AzureBlobStorage
from typing import Dict

def get_label_mapping() -> Dict[str, str]:
    """
    Reads a JSON file containing label mappings from a local path or Azure Blob Storage.

    Returns:
        dict: A dictionary with label mappings, where the key is the label (str) and the value is its corresponding mapping (str).
    """
    config = current_app.config


    if config['LABEL_MAPPING_PATH'].startswith('https://'):
        parsed_url = urlparse(config['LABEL_MAPPING_PATH'])
        path_parts = parsed_url.path.lstrip('/').split('/', 1)
        container_name = path_parts[0]
        blob_name = path_parts[1] if len(path_parts) > 1 else ''
        
        azure_blob_storage = AzureBlobStorage(config['AZURE_STORAGE_CONNECTION_STRING'])
        label_mapping = azure_blob_storage.download_json(container_name, blob_name)
    else:
        # Local file path
        with open(config['LABEL_MAPPING_PATH'], 'r') as f:
            label_mapping = json.load(f)

    return label_mapping
