from ariadne import MutationType
from bson import ObjectId
from datetime import datetime
from config.database import get_db

property_mutation = MutationType()

db = get_db()
property_collection = db["Properties"]

@property_mutation.field("insertProperty")
def resolve_insert_property(_, info, property):
    try:
        property["registered_at"] = datetime.utcnow().isoformat()
        result = property_collection.insert_one(property)
        property["propertyId"] = str(result.inserted_id)
        
        return property
    except Exception as e:
        print(f"Error inserting property: {e}")
        return None

@property_mutation.field("updateProperty")
def resolve_update_property(_, info, propertyId, property):
    try:
        # Prepare the fields that should be updated
        update_fields = {
            "property_name": property.get("property_name"),
            "market_distance": property.get("market_distance"),
            "rent": property.get("rent"),
            "description": property.get("description"),
            "is_available": property.get("is_available"),
            "image_urls": property.get("image_urls"),
        }

        # Remove keys with None values to avoid unnecessary updates
        update_fields = {k: v for k, v in update_fields.items() if v is not None}

        if not update_fields:
            return None  # No fields to update

        update_result = property_collection.update_one(
            {"_id": ObjectId(propertyId)},
            {"$set": update_fields}
        )

        if update_result.modified_count == 1:
            updated_property = property_collection.find_one({"_id": ObjectId(propertyId)})
            updated_property["propertyId"] = str(updated_property["_id"])
            del updated_property["_id"]
            return updated_property
        return None
    except Exception as e:
        print(f"Error updating property: {e}")
        return None

@property_mutation.field("updateImageUrl")
def resolve_update_image_url(_, info, propertyId, image_urls):
    try:
        # Ensure image_urls is a valid list of dictionaries
        if not isinstance(image_urls, list) or not all(isinstance(img, dict) and "url" in img for img in image_urls):
            raise ValueError("Invalid image URLs format. Expected a list of objects with 'url'.")

        update_result = property_collection.update_one(
            {"_id": ObjectId(propertyId)},
            {"$set": {"image_urls": image_urls}}
        )

        if update_result.modified_count == 1:
            updated_property = property_collection.find_one({"_id": ObjectId(propertyId)})
            updated_property["propertyId"] = str(updated_property["_id"])
            del updated_property["_id"]
            return updated_property

        return None
    except Exception as e:
        print(f"Error updating image URLs: {e}")
        return None
    
@property_mutation.field("updateHasAmenities")
def resolve_update_property_amenities(_, info, propertyId, has_amenities):
    try:
        update_result = property_collection.update_one(
            {"_id": ObjectId(propertyId)},
            {"$set": {"has_amenities": has_amenities}}
        )

        if update_result.modified_count == 1:
            updated_property = property_collection.find_one({"_id": ObjectId(propertyId)})
            updated_property["propertyId"] = str(updated_property["_id"])
            del updated_property["_id"]
            return updated_property
        return None
    except Exception as e:
        print(f"Error updating has_amenities: {e}")
        return None

@property_mutation.field("updateIsActive")
def resolve_update_is_active(_, info, propertyId, is_active):
    try:
        update_result = property_collection.update_one(
            {"_id": ObjectId(propertyId)},
            {"$set": {"is_active": is_active}}
        )

        if update_result.modified_count == 1:
            updated_property = property_collection.find_one({"_id": ObjectId(propertyId)})
            updated_property["propertyId"] = str(updated_property["_id"])
            del updated_property["_id"]
            return updated_property
        return None
    except Exception as e:
        print(f"Error updating has_amenities: {e}")
        return None

@property_mutation.field("deleteProperty")
def resolve_delete_property(_, info, propertyId):
    try:
        delete_result = property_collection.delete_one({"_id": ObjectId(propertyId)})
        return delete_result.deleted_count == 1
    except Exception as e:
        print(f"Error deleting property: {e}")
        return False