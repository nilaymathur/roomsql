from pymongo import MongoClient

# MongoDB connection setup
def get_db():
    # uri = "mongodb://localhost:27017/"
    uri = "mongodb+srv://nilaymathur:U3BQfgNWufbmr7Cd@cluster0.aoghk.mongodb.net/myDatabase?retryWrites=true&w=majority"
    client = MongoClient(uri)
    db = client["Properties"]
    return db

