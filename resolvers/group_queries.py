from ariadne import QueryType
from bson import ObjectId
from config.database import get_db

group_query = QueryType()
db = get_db()
groups_collection = db["Groups"]

@group_query.field("getAllGroups")
def resolve_get_all_groups(_, info):
    groups = list(groups_collection.find())
    for group in groups:
        group["_id"] = str(group["_id"])
    return groups

@group_query.field("getGroupById")
def resolve_get_group_by_id(_, info, id):
    group = groups_collection.find_one({"_id": ObjectId(id)})
    if group:
        group["_id"] = str(group["_id"])
    return group

@group_query.field("getMyGroups")
def resolve_get_my_groups(_, info, contact):
    groups = list(groups_collection.find({
        "members.Contact": contact
    }))
    for group in groups:
        group["_id"] = str(group["_id"])
    return groups