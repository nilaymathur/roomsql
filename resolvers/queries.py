from ariadne import QueryType
from bson import ObjectId
from config.database import get_db

# Initialize query type
query = QueryType()

# Database connection
db = get_db()
amenities_collection = db["Amenities"]

@query.field("getFilteredPropertiesByIds")
def resolve_get_filtered_properties_by_ids(_, info, propertyIds):
    try:
        # Extract IDs from the input array
        ids_to_lookup = [prop["propertyId"] for prop in propertyIds]
        
        # Query MongoDB to find matching properties by their IDs
        properties = list(amenities_collection.find({"propertyId": {"$in": ids_to_lookup}}))

        return properties
    except Exception as e:
        print(f"Error querying properties: {e}")
        return []



@query.field("getPropertyById")
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
