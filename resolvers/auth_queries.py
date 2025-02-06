from ariadne import QueryType
# from bson import ObjectId
from config.database import get_db

# Initialize query type
auth_query = QueryType()

# Database connection
db = get_db()
users_collection = db["Users"]

@auth_query.field("getUser")
def resolve_get_user(_, info, aadhar_no):
    users = list(users_collection.find({"aadhar_no": aadhar_no}))  # Convert cursor to list

    if users:  # Ensure we have results
        result = []
        for user in users:
            result.append({
                "active": user.get("active", False),
                "email": user.get("email", ""),
                "mobile":user.get("_id", ""),
                "name":user.get("name", ""),
                "profile_uri": user.get("profile_uri", ""),
                "role": user.get("role", ""),
            })
        return result
    return []

@auth_query.field("login")
def resolve_login(_, info, mobile, password):
    user = users_collection.find_one({"_id": mobile, "password": password})

    if user:
        return {
            "aadhar_no": user.get("aadhar_no", ""),
            "active": user.get("active", False),
            "email": user.get("email", ""),
            "mobile": user.get("mobile", ""),
            "name": user.get("name", ""),
            "profile_uri": user.get("profile_uri", ""),
            "role": user.get("role", ""),
        }
    
    return None  # Returns `null` in GraphQL response if login fails

