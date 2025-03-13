from ariadne import MutationType
from bson import ObjectId
from datetime import datetime
from config.database import get_db

worldcity_mutation = MutationType()
db = get_db()
worldcities_collection = db["worldcities"]

@worldcity_mutation.field("insertWorldCity")
def resolve_insert_worldcity(_, info, cityData):
    try:
        cityData["registeredOn"] = datetime.utcnow().isoformat()
        result = worldcities_collection.insert_one(cityData)
        cityData["id"] = str(result.inserted_id)
        
        return cityData
    except Exception as e:
        print(f"Error inserting city: {e}")
        return None
