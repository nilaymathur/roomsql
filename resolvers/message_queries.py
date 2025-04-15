from ariadne import QueryType
from bson import ObjectId
from config.database import get_db

message_query = QueryType()
db = get_db()
messages_collection = db["Messages"]

@message_query.field("getMessagesBySenderReceiverAndDateRange")
def resolve_get_messages_by_sender_receiver_and_date_range(_, info, senderContact, receiverContact, startDate, endDate):
    # Convert string dates to datetime objects
    start_date = datetime.fromisoformat(startDate)
    end_date = datetime.fromisoformat(endDate)

    # Find messages exchanged between the sender and receiver within the date range
    query = {
        "senderContact": senderContact,
        "receivers.Contact": receiverContact,
        "time": {"$gte": start_date, "$lte": end_date}
    }

    # Fetch messages from the database
    messages = list(messages_collection.find(query))

    # Return messages with properly formatted IDs and Date
    for msg in messages:
        msg["_id"] = str(msg["_id"])
        msg["time"] = msg["time"].isoformat()  # Convert datetime to ISO string
    return messages

@message_query.field("getMessagesBySenderReceiver")
def resolve_get_messages_by_sender_receiver(_, info, senderContact, receiverContact):
    # Find messages exchanged between the sender and receiver without considering dates
    query = {
        "$or": [
            {"senderContact": senderContact, "receivers.Contact": receiverContact},
            {"senderContact": receiverContact, "receivers.Contact": senderContact}
        ]
    }

    # Fetch messages from the database
    messages = list(messages_collection.find(query))

    # Return messages with properly formatted IDs
    for msg in messages:
        msg["_id"] = str(msg["_id"])
        msg["time"] = msg["time"].isoformat()  # Convert datetime to ISO string
    return messages

@message_query.field("getMyMessages")
def resolve_get_my_messages(_, info, contact):
    messages = list(messages_collection.find({
        "$or": [
            {"senderContact": contact},
            {"receivers.Contact": contact}
        ]
    }))
    
    for msg in messages:
        msg["_id"] = str(msg["_id"])
    return messages
