from ariadne import QueryType
from bson import ObjectId
from config.database import get_db

message_query = QueryType()
db = get_db()
messages_collection = db["Messages"]

@message_query.field("getGroupMessages")
def resolve_get_group_messages(_, info, contact):
    messages = list(messages_collection.find({
        "receivers.Contact": contact,
        "groupId": {"$ne": None}  # groupId should not be null
    }))
    for msg in messages:
        msg["_id"] = str(msg["_id"])
    return messages

@message_query.field("getIndividualMessages")
def resolve_get_individual_messages(_, info, sender, receiver):
    messages = list(messages_collection.find({
        "$or": [
            {"senderContact": sender, "receivers.Contact": receiver},
            {"senderContact": receiver, "receivers.Contact": sender}
        ],
        "groupId": None  # No groupId for personal chat
    }))
    for msg in messages:
        msg["_id"] = str(msg["_id"])
    return messages

@message_query.field("getMyMessages")
def resolve_get_my_messages(_, info, contact):
    # You can access your database or data source here
    # Example placeholder logic:
    return fetch_messages_for_contact(contact)


@message_query.field("getMessagesSinceLastMonth")
def resolve_get_messages_since_last_month(_, info, contact):
    # Fetch all messages
    messages = fetch_messages_for_contact(contact)
    
    # Filter messages from the last month
    from datetime import datetime, timedelta
    one_month_ago = datetime.now() - timedelta(days=30)

    # Assuming each message has a 'timeStamp' field
    recent_messages = [
        msg for msg in messages if datetime.fromisoformat(msg["timeStamp"]) >= one_month_ago
    ]
    
    return recent_messages

