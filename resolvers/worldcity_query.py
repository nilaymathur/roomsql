from ariadne import QueryType
from bson import ObjectId
from config.database import get_db

worldcity_query = QueryType()
db = get_db()
worldcities_collection = db["worldcities"]

@worldcity_query.field("getCityByFilters")
def resolve_get_city_by_filters(_, info, country, state, city):
    try:
        query = {
            "country": country,
            "state": state,
            "city": city
        }
        cities = list(worldcities_collection.find(query))
        
        for city in cities:
            city["id"] = str(city["_id"])
            del city["_id"]

        return cities
    except Exception as e:
        print(f"Error fetching city: {e}")
        return []

@worldcity_query.field("getCountries")
def resolve_get_countries(_, info):
    try:
        countries = worldcities_collection.distinct("country")
        return countries
    except Exception as e:
        print(f"Error fetching countries: {e}")
        return []

@worldcity_query.field("getStates")
def resolve_get_states(_, info, country):
    try:
        states = worldcities_collection.distinct("state", {"country": country})
        return states
    except Exception as e:
        print(f"Error fetching states: {e}")
        return []

@worldcity_query.field("getCities")
def resolve_get_cities(_, info, country, state):
    try:
        cities = worldcities_collection.distinct("city_ascii", {"country": country, "state": state})
        return cities
    except Exception as e:
        print(f"Error fetching cities: {e}")
        return []