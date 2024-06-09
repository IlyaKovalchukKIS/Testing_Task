import bson
from pymongo import MongoClient


def create_db(
    host: str = "localhost",
    port: int = 27017,
    db_name: str = None,
    collection: str = None,
    filename_collection: str = None,
):
    connect = MongoClient(f"mongodb://{host}:{port}")
    collection = connect[db_name][collection]
    with open(filename_collection, "rb") as f:
        data = bson.decode_all(f.read())

    collection.insert_many(data)
