from ariadne import QueryType
from bson import ObjectId
from config.database import get_db

# Initialize query type
amenity_query = QueryType()

# Database connection
db = get_db()
amenities_collection = db["Amenities"]

@amenity_query.field("getAmenityById")
def resolve_get_amenity_by_propertyId(_, info, propertyId):
    try:
        # Query MongoDB
        amenity = amenities_collection.find_one({"propertyId": propertyId})

        # Handle response if property exists
        if amenity:
            # Convert the ObjectId to a string for GraphQL compatibility
            amenity["_id"] = str(amenity["_id"])
            return amenity
        else:
            # Return an empty response if no amenity is found
            return None
    except Exception as e:
        print(f"Error fetching amenity by id: {e}")
        return None
