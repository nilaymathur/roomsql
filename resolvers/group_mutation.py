from ariadne import MutationType
from bson import ObjectId
from datetime import datetime
from config.database import get_db

group_mutation = MutationType()
db = get_db()
groups_collection = db["Groups"]

@group_mutation.field("createGroup")
def resolve_create_group(_, info, groupName, members, displayPicture=None):
    new_group = {
        "isGroup": True,
        "groupName": groupName,
        "members": members,
        "displayPicture": displayPicture,
        "createdAt": datetime.utcnow().isoformat(),
        "updatedAt": datetime.utcnow().isoformat()
    }
    result = groups_collection.insert_one(new_group)
    new_group["_id"] = str(result.inserted_id)
    return new_group

@group_mutation.field("deleteGroup")
def resolve_delete_group(_, info, id):
    result = groups_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count == 1


@group_mutation.field("updateGroupName")
def resolve_update_group_name(_, info, id, groupName):
    result = groups_collection.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "groupName": groupName,
                "updatedAt": datetime.utcnow().isoformat()
            }
        }
    )
    if result.matched_count == 1:
        updated_group = groups_collection.find_one({"_id": ObjectId(id)})
        updated_group["_id"] = str(updated_group["_id"])
        return updated_group
    return None
