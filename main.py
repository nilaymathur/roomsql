import uvicorn
from fastapi import FastAPI
from ariadne.asgi import GraphQL
from config.database import get_db
from fastapi.middleware.cors import CORSMiddleware
from ariadne import make_executable_schema, load_schema_from_path, upload_scalar, QueryType 

from resolvers.amenity_queries import amenity_query
from resolvers.amenity_mutations import amenity_mutation

from resolvers.auth_queries import auth_query
from resolvers.auth_mutation import auth_mutation

from resolvers.image_mutation import image_mutation as img_mutation
from resolvers.image_query import image_query as img_query

# Load the schema from schema.graphql
amenity_defs = load_schema_from_path("schemas/amenity_schema.graphql")
auth_defs = load_schema_from_path("schemas/auth_schema.graphql")
image_defs = load_schema_from_path("schemas/image_schema.graphql")


# Create the executable schema
auth_schema = make_executable_schema(auth_defs, auth_query, auth_mutation)
image_schema = make_executable_schema(image_defs, img_query, img_mutation, upload_scalar)
amenity_schema = make_executable_schema(amenity_defs, amenity_query, amenity_mutation)

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/routes")
def get_routes():
    return [{"path": route.path, "name": route.name} for route in app.router.routes]

# Add GraphQL endpoint
app.add_route("/amenity_graphql", GraphQL(amenity_schema, debug=False))
app.add_route("/auth_graphql", GraphQL(auth_schema, debug=False))
app.add_route("/image_graphql", GraphQL(image_schema, debug=False))

# MongoDB connection check (optional)
@app.on_event("startup")
def startup_event():
    db = get_db()
    print("MongoDB connected:", db.name)
