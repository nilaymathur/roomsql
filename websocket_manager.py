from fastapi import WebSocket
from typing import List

# List to store active WebSocket connections
active_connections: List[WebSocket] = []

async def connect(websocket: WebSocket):
    """Add a new WebSocket connection."""
    await websocket.accept()
    active_connections.append(websocket)

async def disconnect(websocket: WebSocket):
    """Remove a WebSocket connection."""
    active_connections.remove(websocket)

async def broadcast(message: str, sender: WebSocket):
    """Broadcast a message to all connected clients except the sender."""
    for connection in active_connections:
        if connection != sender:
            await connection.send_text(message)