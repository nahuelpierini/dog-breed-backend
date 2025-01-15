from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.core.exceptions import AzureError
from uuid import uuid4
from typing import Any, Dict
import json

class AzureBlobStorage:
    """
    A class to interact with Azure Blob Storage for uploading files.
    """

    def __init__(self, connection_string: str) -> None:
        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            print("Successfully connected to Blob Storage.")
        except AzureError as e:
            raise Exception(f"Error connecting to Blob Storage: {str(e)}")

    def upload_file(self, file: Any, breed: str) -> str:
        file_name = f"{breed}/{uuid4()}_{file.filename}"
        blob_client = self.container_client.get_blob_client(file_name)
        blob_client.upload_blob(file)
        return blob_client.url

    def upload_image(self, container_name: str, folder_name: str, blob_name: str, file_data: Any, content_type: str) -> None:
        try:
            extension = content_type.split("/")[-1]
            if extension not in ["jpeg", "png", "jpg"]:
                raise ValueError(f"Unsupported file type: {content_type}")
            blob_name_with_extension = f"{folder_name}/{uuid4()}_{blob_name}.{extension}"

            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name_with_extension)
            blob_client.upload_blob(
                file_data,
                overwrite=True,
                content_settings=ContentSettings(content_type=content_type)
            )
            print(f"Image '{blob_name_with_extension}' successfully uploaded to container '{container_name}'.")
        except AzureError as e:
            print(f"Error uploading image '{blob_name}': {str(e)}")
        except ValueError as e:
            print(f"Error processing file '{blob_name}': {str(e)}")


    def download_json(self, container_name: str, blob_name: str) -> Dict[str, Any]:
        """
        Downloads a JSON file from a blob container and parses its content.

        Args:
            container_name (str): The name of the container.
            blob_name (str): The name of the blob.

        Returns:
            dict: The content of the JSON file as a dictionary.
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
            blob_data = blob_client.download_blob().readall()
            json_data = json.loads(blob_data)
            print(f"Successfully downloaded JSON blob '{blob_name}' from container '{container_name}'.")
            return json_data
        except AzureError as e:
            raise Exception(f"Error downloading JSON blob '{blob_name}': {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Error decoding JSON blob '{blob_name}': {str(e)}")