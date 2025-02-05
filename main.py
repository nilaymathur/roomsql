from fastapi import FastAPI
from ariadne.asgi import GraphQL
from config.database import get_db
from fastapi.middleware.cors import CORSMiddleware
from ariadne import make_executable_schema, load_schema_from_path

from resolvers.amenity_queries import amenity_query
from resolvers.amenity_mutations import amenity_mutation

from resolvers.auth_queries import auth_query
from resolvers.auth_mutation import auth_mutation

# Load the schema from schema.graphql
amenity_defs = load_schema_from_path("schemas/amenity_schema.graphql")
auth_defs = load_schema_from_path("schemas/auth_schema.graphql")

# Create the executable schema
amenity_schema = make_executable_schema(amenity_defs, amenity_query, amenity_mutation)
auth_schema = make_executable_schema(auth_defs, auth_query, auth_mutation)

# Initialize FastAPI app
app = FastAPI()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return "Server is up and running"

@app.get("/routes")
def get_routes():
    return [{"path": route.path, "name": route.name} for route in app.router.routes]

# Add GraphQL endpoint
app.add_route("/amenity_graphql", GraphQL(amenity_schema, debug=True))
app.add_route("/auth_graphql", GraphQL(auth_schema, debug=True))

# MongoDB connection check (optional)
@app.on_event("startup")
def startup_event():
    db = get_db()
    print("MongoDB connected:", db.name)