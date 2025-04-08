from ariadne import MutationType
from websocket_manager import broadcast, active_connections

chat_mutation = MutationType()

@chat_mutation.field("sendMessage")
async def resolve_send_message(_, info, user_id, message):
    # Broadcast the message to all WebSocket clients
    for connection in active_connections:
        try:
            await broadcast(f"{user_id}: {message}", connection)
        except Exception as e:
            print(f"Error broadcasting message: {e}")

    # Return the message and user_id as a response
    return {
        "user_id": user_id,
        "message": message
    }