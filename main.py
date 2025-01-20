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
    # allow_origins=["*"],  # Replace "*" with specific origins for production
    allow_origins=["http://localhost:53197", "*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Add GraphQL endpoint
app.add_route("/graphql", GraphQL(schema, debug=False))

# MongoDB connection check (optional)
@app.on_event("startup")
def startup_event():
    db = get_db()
    print("MongoDB connected:", db.name)
