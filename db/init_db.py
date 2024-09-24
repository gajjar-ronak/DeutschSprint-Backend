from pymongo import MongoClient
from core.config import settings

# Initialize MongoDB client and db globally
client = None
db = None

def init_db():
    """
    Initialize the MongoDB client and database.
    """
    global client, db
    if client is None:
        client = MongoClient(settings.MONGO_URI)
        db = client[settings.DATABASE_NAME]
    return db

def close_db():
    """
    Closes the MongoDB client connection.
    """
    global client
    if client:
        client.close()
        client = None

def create_collection(collection_name: str):
    """
    Create a collection if it does not exist.
    """
    init_db()
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)

def drop_collection(collection_name: str):
    """
    Drop a collection if it exists.
    """
    init_db()
    if collection_name in db.list_collection_names():
        db[collection_name].drop()

def get_collection(collection_name: str):
    """
    Get a MongoDB collection.
    """
    init_db()
    return db[collection_name]

# CRUD Operations

def insert_one(collection_name: str, document: dict):
    """
    Insert one document into a collection.
    """
    collection = get_collection(collection_name)
    return collection.insert_one(document)

def insert_many(collection_name: str, documents: list):
    """
    Insert many documents into a collection.
    """
    collection = get_collection(collection_name)
    return collection.insert_many(documents)

def find_one(collection_name: str, query: dict):
    """
    Find a single document based on a query.
    """
    collection = get_collection(collection_name)
    return collection.find_one(query)

def find_many(collection_name: str, query: dict = {}):
    """
    Find multiple documents based on a query.
    """
    collection = get_collection(collection_name)
    return list(collection.find(query))

def update_one(collection_name: str, query: dict, update_data: dict):
    """
    Update a single document in a collection.
    """
    collection = get_collection(collection_name)
    return collection.update_one(query, {"$set": update_data})

def update_many(collection_name: str, query: dict, update_data: dict):
    """
    Update multiple documents in a collection.
    """
    collection = get_collection(collection_name)
    return collection.update_many(query, {"$set": update_data})

def delete_one(collection_name: str, query: dict):
    """
    Delete a single document from a collection.
    """
    collection = get_collection(collection_name)
    return collection.delete_one(query)

def delete_many(collection_name: str, query: dict):
    """
    Delete multiple documents from a collection.
    """
    collection = get_collection(collection_name)
    return collection.delete_many(query)


def get_vocab_collection():
    db = init_db()
    return db["vocabulary"]  # Replace "vocabulary" with the actual name of your collection