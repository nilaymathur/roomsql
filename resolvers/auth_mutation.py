from ariadne import MutationType
from config.database import get_db
from bson import ObjectId

# Initialize mutation type
auth_mutation = MutationType()

# Database connection
db = get_db()
users_collection = db["Users"]

@auth_mutation.field("createUser")
def resolve_create_user(_, info, aadhar_no, active, email, mobile, name, password, profile_uri, role):
    new_user = {
        "_id": mobile,
        "aadhar_no": aadhar_no,
        "active": active,
        "email": email,
        "name": name,
        "password": password,
        "profile_uri": profile_uri,
        "role": role
    }
    result = users_collection.insert_one(new_user)
    return result.acknowledged

@auth_mutation.field("updateUser")
def resolve_update_user(_, info, active, email, mobile, password, profile_uri):
    update_result = users_collection.update_one(
        {"_id": mobile},
        {"$set": {
            "active": active,
            "email": email,
            "password": password,
            "profile_uri": profile_uri,
        }}
    )
    return update_result.modified_count > 0

# @auth_mutation.field("login")
# def resolve_login(_, info, mobile, password):
#     user = users_collection.find_one({"_id": mobile})

#     if not user:
#         return False
    
#     if user['password'] == password:
#         return True
#     return False

@auth_mutation.field("deleteUser")
def resolve_delete_user(_, info, mobile):
    delete_result = users_collection.delete_one({"_id": mobile})
    return delete_result.deleted_count > 0
