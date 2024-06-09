import os
from datetime import datetime

import bson
from pymongo import MongoClient, errors
from dotenv import load_dotenv

load_dotenv()


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

    collection.drop()
    collection.insert_many(data)


def func_sale(dt_from: str, dt_upto: str, group_type: str):
    connect = MongoClient("mongodb://localhost:27017")
    collection = connect[os.getenv("NAME_DB")][os.getenv("COLLECTION_DB")]

    start_datetime = datetime.strptime(dt_from, "%Y-%m-%dT%H:%M:%S")
    end_datetime = datetime.strptime(dt_upto, "%Y-%m-%dT%H:%M:%S")

    pipeline = []
    group_stage = {
        "$group": {
            "_id": "",
            "total_sales": {"$sum": "$value"},
            "sale_dates": {"$push": "$dt"},
        }
    }

    if group_type == "hour":
        group_stage["$group"]["_id"] = {
            "$dateToString": {"format": "%Y-%m-%dT%H:00:00", "date": "$dt"}
        }
    elif group_type == "day":
        group_stage["$group"]["_id"] = {
            "$dateToString": {"format": "%Y-%m-%dT00:00:00", "date": "$dt"}
        }
    elif group_type == "month":
        group_stage["$group"]["_id"] = {
            "$dateToString": {"format": "%Y-%m-01T00:00:00", "date": "$dt"}
        }
    else:
        raise ValueError("Unsupported group_type")

    pipeline.append({"$match": {"dt": {"$gte": start_datetime, "$lte": end_datetime}}})
    pipeline.append(group_stage)

    try:
        result = collection.aggregate(pipeline)
        total_sales = []
        sale_dates = []

        for item in result:
            total_sales.append(item["total_sales"])
            sale_dates.append(item["_id"])

        return {"dataset": total_sales, "labels": sale_dates}

    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")
