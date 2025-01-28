from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ariadne import make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL
from resolvers.queries import query
from resolvers.mutations import mutation
from config.database import get_db

# Load the schema from schema.graphql
type_defs = load_schema_from_path("schema.graphql")

# Create the executable schema
schema = make_executable_schema(type_defs, query, mutation)

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
    return {"Property": "Amenities"}

@app.get("/routes")
def get_routes():
    return [{"path": route.path, "name": route.name} for route in app.router.routes]

# Add GraphQL endpoint
app.add_route("/graphql", GraphQL(schema, debug=True))

# MongoDB connection check (optional)
@app.on_event("startup")
def startup_event():
    db = get_db()
    print("MongoDB connected:", db.name)