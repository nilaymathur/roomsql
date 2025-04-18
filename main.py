import asyncio

from typing import List
from datetime import datetime

from ariadne.asgi import GraphQL
from config.database import get_db
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from ariadne import make_executable_schema, load_schema_from_path, upload_scalar, QueryType

from resolvers.property_mutation import property_mutation
from resolvers.property_query import property_query

from resolvers.worldcity_mutation import worldcity_mutation
from resolvers.worldcity_query import worldcity_query

from resolvers.auth_queries import auth_query
from resolvers.auth_mutation import auth_mutation

from resolvers.amenity_queries import amenity_query
from resolvers.amenity_mutations import amenity_mutation

from resolvers.message_queries import message_query
from resolvers.message_mutation import message_mutation

from resolvers.group_queries import group_query
from resolvers.group_mutation import group_mutation

# create a function to add two numbers

# Load the schema from schema.graphql
amenity_defs = load_schema_from_path("schemas/amenity_schema.graphql")
auth_defs = load_schema_from_path("schemas/auth_schema.graphql")
property_defs = load_schema_from_path("schemas/property_schema.graphql")
worldcity_defs = load_schema_from_path("schemas/worldcities_schema.graphql")
message_defs = load_schema_from_path("schemas/message_schema.graphql")
group_defs = load_schema_from_path("schemas/group_schema.graphql")

# Create the executable schema
auth_schema = make_executable_schema(auth_defs, auth_query, auth_mutation)
amenity_schema = make_executable_schema(amenity_defs, amenity_query, amenity_mutation)
property_schema = make_executable_schema(property_defs, property_query, property_mutation)
worldcity_schema = make_executable_schema(worldcity_defs, worldcity_query, worldcity_mutation)
message_schema = make_executable_schema(message_defs, message_query, message_mutation)
group_scheam = make_executable_schema(group_defs, group_query, group_mutation)

# Initialize FastAPI app
app = FastAPI()

app.add_route("/amenity_graphql", GraphQL(amenity_schema, debug=False))
app.add_route("/auth_graphql", GraphQL(auth_schema, debug=False))
app.add_route("/property_graphql", GraphQL(property_schema, debug=False))
app.add_route("/worldcity_graphql", GraphQL(worldcity_schema, debug=False))
app.add_route("/message_graphql", GraphQL(message_schema, debug=False))
app.add_route("/group_graphql", GraphQL(group_scheam, debug=False))

active_connections: list[WebSocket] = []

# WebSocket Chat Hub Section
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print("🟢 Connection opened. Total active:", len(active_connections))

    try:

        asyncio.create_task(ping_clients())

        while True:
            message = await websocket.receive_text()
            for connection in active_connections:
                try:
                    await connection.send_text(message)
                except Exception as e:
                    print(f"⚠️ Failed to send to client: {e}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        if websocket in active_connections:
            active_connections.remove(websocket)

# Ping all clients every 20 seconds to keep connection alive
async def ping_clients():
    while True:
        await asyncio.sleep(20)
        for connection in active_connections:
            try:
                await connection.send_text("__ping__")
                print("📡 Ping sent to keep connection alive")
            except Exception as e:
                print(f"⚠️ Ping failed: {e}")

# MongoDB connection check (optional)
@app.on_event("startup")
def startup_event():
    db = get_db()
    # asyncio.create_task(chat_client())
    print("MongoDB connected:", db.name)