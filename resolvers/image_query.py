from ariadne import QueryType
from azure.storage.blob import ContainerClient

# Initialize QueryType
image_query = QueryType()

# Azure Blob Storage Connection String
BLOB_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=roomsstore;AccountKey=3Cd5PHpfEg9ThFaI7nO+nGdb0PRkwQy4VlQkdjWPJLq0zNKTYPSi6pITKoEBh/z9mPrEdDq4Xfnp+ASt4fqJYQ==;EndpointSuffix=core.windows.net"

@image_query.field("getImages")
def resolve_get_images(_, info, containerName):
    try:
        # Initialize Container Client with dynamic container name
        container_client = ContainerClient.from_connection_string(
            BLOB_CONNECTION_STRING, container_name=containerName
        )
        
        # Fetch blobs from the container
        blobs = container_client.list_blobs()
        return [blob.name for blob in blobs]  # Return list of blob names
    
    except Exception as e:
        print(f"Error fetching images from {containerName}: {str(e)}")
        return []
