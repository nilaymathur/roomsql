from ariadne import MutationType
from bson import ObjectId
from config.database import get_db

message_mutation = MutationType()
db = get_db()
messages_collection = db["Messages"]

@message_mutation.field("createMessage")
def resolve_create_message(_, info, senderName, senderContact, receivers, status, message, time):
    new_message = {
        "senderName": senderName,
        "senderContact": senderContact,
        "receivers": receivers,
        "status": status,
        "message": message,
        "time": time
    }
    result = messages_collection.insert_one(new_message)
    return result.acknowledged

@message_mutation.field("updateMessageContent")
def resolve_update_message_content(_, info, id, message):
    result = messages_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"message": message}}
    )
    return result.modified_count > 0

@message_mutation.field("updateMessageStatus")
def resolve_update_message_status(_, info, id, status):
    result = messages_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": status}}
    )
    return result.modified_count > 0

@message_mutation.field("deleteMessage")
def resolve_delete_message(_, info, id):
    result = messages_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0

@message_mutation.field("markAllMessagesAsRead")
def resolve_mark_all_messages_as_read(_, info, receiverContact):
    result = messages_collection.update_many(
        {
            "receivers.Contact": receiverContact,
            "status": "sent"
        },
        {
            "$set": { "status": "read" }
        }
    )
    return result.acknowledged