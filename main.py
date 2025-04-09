import asyncio

from typing import Dict, List
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


# create a function to add two numbers

# Load the schema from schema.graphql
amenity_defs = load_schema_from_path("schemas/amenity_schema.graphql")
auth_defs = load_schema_from_path("schemas/auth_schema.graphql")
property_defs = load_schema_from_path("schemas/property_schema.graphql")
worldcity_defs = load_schema_from_path("schemas/worldcities_schema.graphql")


# Create the executable schema

auth_schema = make_executable_schema(auth_defs, auth_query, auth_mutation)
amenity_schema = make_executable_schema(amenity_defs, amenity_query, amenity_mutation)
property_schema = make_executable_schema(property_defs, property_query, property_mutation)
worldcity_schema = make_executable_schema(worldcity_defs, worldcity_query, worldcity_mutation)

# Initialize FastAPI app
app = FastAPI()

app.add_route("/amenity_graphql", GraphQL(amenity_schema, debug=False))
app.add_route("/auth_graphql", GraphQL(auth_schema, debug=False))
app.add_route("/property_graphql", GraphQL(property_schema, debug=False))
app.add_route("/worldcity_graphql", GraphQL(worldcity_schema, debug=False))

active_connections: list[WebSocket] = []

# WebSocket Chat Hub Section
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print("active_connections:", active_connections)

    try:
        while True:
            message = await websocket.receive_text()
            for connection in active_connections:
                await connection.send_text(message)
    except:
        active_connections.remove(websocket)

# MongoDB connection check (optional)
@app.on_event("startup")
def startup_event():
    db = get_db()
    # asyncio.create_task(chat_client())
    print("MongoDB connected:", db.name)