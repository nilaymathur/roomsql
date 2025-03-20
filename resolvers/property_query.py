from ariadne import QueryType
from bson import ObjectId
from config.database import get_db

property_query = QueryType()

db = get_db()
property_collection = db["Properties"]

@property_query.field("getPropertyById")
def resolve_get_property_by_id(_, info, propertyId):
    try:
        property_data = property_collection.find_one({"_id": ObjectId(propertyId)})
        
        if property_data:
            property_data["propertyId"] = str(property_data["_id"])  # Rename _id to propertyId
            del property_data["_id"]  # Remove _id to avoid redundancy
            return property_data
        return None
    except Exception as e:
        print(f"Error fetching property by id: {e}")
        return None

@property_query.field("getPropByLT")
def resolve_get_prop_by_lt(_, info, type, city, state, country):
    print(type, city, state, country)
    try:
        # Case-insensitive search using $regex with $options: "i"
        filtered_properties = list(property_collection.find({
            "type": { "$regex": f"^{type}$", "$options": "i" },
            "address.city": { "$regex": f"^{city}$", "$options": "i" },
            "address.state": { "$regex": f"^{state}$", "$options": "i" },
            "address.country": { "$regex": f"^{country}$", "$options": "i" }
        }))

        print(filtered_properties)

        # Convert MongoDB ObjectId to string and rename `_id` to `propertyId`
        for property in filtered_properties:
            property["propertyId"] = str(property["_id"])
            del property["_id"]

        return filtered_properties
    except Exception as e:
        print(f"Error fetching properties by location and type: {e}")
        return []

@property_query.field("getAllProperties")
def resolve_get_all_properties(_, info):
    try:
        properties = list(property_collection.find({}))
        for property in properties:
            property["propertyId"] = str(property["_id"])
            del property["_id"]
        return properties
    except Exception as e:
        print(f"Error fetching all properties: {e}")
        return []

@property_query.field("getPropertyCount")
def resolve_get_property_count(_, info, owner_id):
    try:
        total_count = property_collection.count_documents({"owner_id": owner_id})
        active_count = property_collection.count_documents({"owner_id": owner_id, "is_active": True})
        return {
             "count": total_count,
            "is_active": active_count
        }
    except Exception as e:
        print(f"Error fetching property by id: {e}")
        return {
            "count": 0,
            "is_active": 0
        }

@property_query.field("getMyProperties")
def resolve_get_my_properties(_, info, owner_id):
    try:
        # Query MongoDB with given filters
        filtered_properties = list(property_collection.find({
            "owner_id": owner_id
        }))

        # Convert MongoDB ObjectId to string and rename `_id` to `propertyId`
        for property in filtered_properties:
            property["propertyId"] = str(property["_id"])
            del property["_id"]

        return filtered_properties
    except Exception as e:
        print(f"Error fetching your properties: {e}")
        return []