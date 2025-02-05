from ariadne import QueryType
from bson import ObjectId
from config.database import get_db

# Initialize query type
amenity_query = QueryType()

# Database connection
db = get_db()
amenities_collection = db["Amenities"]

@amenity_query.field("getPropertyById")
def resolve_get_property_by_propertyId(_, info, propertyId):
    try:
        # Query MongoDB
        property = amenities_collection.find_one({"propertyId": propertyId})

        # Handle response if property exists
        if property:
            # Convert the ObjectId to a string for GraphQL compatibility
            property["_id"] = str(property["_id"])
            return property
        else:
            # Return an empty response if no property is found
            return None
    except Exception as e:
        print(f"Error fetching property by id: {e}")
        return None
