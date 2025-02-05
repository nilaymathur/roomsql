from ariadne import MutationType
from bson import ObjectId
from config.database import get_db

# Initialize mutation type
amenity_mutation = MutationType()

# Database connection
db = get_db()
students_collection = db["Amenities"]

@amenity_mutation.field("insertAmenity")
def resolve_create_amenity(_, info, propertyId, amenities):
    try:
        # Validate input
        if not amenities:
            return {"error": "Amenities list cannot be empty."}

        # Map amenities and their checkboxes properly
        new_amenities = []
        for amenity in amenities:
            # Extract the required fields for each amenity and ensure all are mapped correctly
            new_amenity = {
                "title": amenity.get("title"),
                "checkboxes": [
                    {
                        "amenityName": checkbox.get("amenityName"),
                        "hasAmenity": checkbox.get("hasAmenity", False),
                    }
                    for checkbox in amenity.get("checkboxes", [])
                ]
            }
            new_amenities.append(new_amenity)

        # Prepare final amenity object
        final_amenity = {
            "propertyId": propertyId,
            "amenities": new_amenities
        }

        # Insert the data into the database
        result = students_collection.insert_one(final_amenity)

        # Return the inserted data for confirmation
        final_amenity["_id"] = str(result.inserted_id)  # Convert the database ID to string
        return final_amenity
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}


# Resolver for updateAmenity
@amenity_mutation.field("updateAmenity")
def resolve_update_amenity(_, info, propertyId, amenities):
    try:
        if not amenities:
            return {"error": "Amenities list cannot be empty for update."}

        # Map amenities data properly
        updated_amenities = [
            {
                "title": amenity.get("title"),
                "checkboxes": [
                    {
                        "amenityName": checkbox.get("amenityName"),
                        "hasAmenity": checkbox.get("hasAmenity", False),
                    }
                    for checkbox in amenity.get("checkboxes", [])
                ]
            }
            for amenity in amenities
        ]

        # Perform the database update
        result = students_collection.update_one(
            {"propertyId": propertyId},
            {"$set": {"amenities": updated_amenities}},
            upsert=True  # Insert if no record exists
        )

        if result.modified_count >= 0:
            # Return the updated record
            updated_property = students_collection.find_one({"propertyId": propertyId})
            updated_property["_id"] = str(updated_property["_id"])
            return updated_property
        else:
            return {"error": "No updates were made."}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}


# Resolver for deleteAmenity
@amenity_mutation.field("deleteAmenity")
def resolve_delete_amenity(_, info, propertyId):
    try:
        # Delete all amenities under a given propertyId
        result = students_collection.delete_one({"propertyId": propertyId})

        if result.deleted_count > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False