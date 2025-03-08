from ariadne import MutationType
from azure.storage.blob import BlobServiceClient
import os

# Azure Blob Storage Connection String
BLOB_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=roomsstore;AccountKey=3Cd5PHpfEg9ThFaI7nO+nGdb0PRkwQy4VlQkdjWPJLq0zNKTYPSi6pITKoEBh/z9mPrEdDq4Xfnp+ASt4fqJYQ==;EndpointSuffix=core.windows.net"

# Initialize Mutation Type
image_mutation = MutationType()

@image_mutation.field("uploadImage")
async def resolve_upload_image(_, info, file, imageName, containerName):
    try:
        # Read file contents
        file_contents = await file.read()

        # Initialize Blob Service Client
        blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(containerName)

        # Upload file to Azure Blob Storage
        blob_client = container_client.get_blob_client(imageName)
        blob_client.upload_blob(file_contents, overwrite=True)

        # Construct file URL
        blob_url = f"https://roomsstore.blob.core.windows.net/{containerName}/{imageName}"

        return {
            "success": True,
            "message": "File uploaded successfully!",
            "url": blob_url
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Upload failed: {str(e)}",
            "url": None
        }
    
@image_mutation.field("deleteImage")
def resolve_delete_image(_, info, imageName, containerName):
    try:
        # Initialize Blob Service Client
        blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(containerName)

        # Get blob client for the image
        blob_client = container_client.get_blob_client(imageName)

        # Check if blob exists
        if not blob_client.exists():
            return {
                "success": False,
                "message": "Image not found!"
            }

        # Delete the blob
        blob_client.delete_blob()

        return {
            "success": True,
            "message": "Image deleted successfully!"
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Deletion failed: {str(e)}"
        }
