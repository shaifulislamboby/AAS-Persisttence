import datetime
import logging
from apscheduler.schedulers.background import BackgroundScheduler


from django.conf import settings

from django.http import JsonResponse
from pymongo import MongoClient

from main.helpers import (
    get_or_create_database_collection,
    insert_document_in_collection,
)


def get_data(request, collection_name: str = "aas_collection"):
    database_name = "aas_database"

    client = MongoClient(settings.MONGO_URL)
    db = client[database_name]
    collection = db[collection_name]
    get_or_create_database_collection(
        database_name="aas_database", collection_name=collection_name
    )
    # Retrieve data from MongoDB collection
    data_from_mongo = list(collection.find())

    # Convert MongoDB documents to JSON-compatible format
    json_data = [{k: str(v) for k, v in doc.items()} for doc in data_from_mongo]

    # Close the MongoDB connection
    client.close()

    return JsonResponse(json_data, safe=False)


def save_data(
    request,
    aas_collection_name: str = "aas_collection",
    submodel_collection_name: str = "submodel_collection",
):
    # Create a scheduler
    scheduler = BackgroundScheduler()

    # Add the background task to the scheduler
    scheduler.add_job(
        data_saving_task,
        "interval",
        seconds=settings.DATA_UPDATE_INTERVAL,
        args=(aas_collection_name, submodel_collection_name),
    )

    # Start the scheduler
    scheduler.start()

    return JsonResponse({"success": "successfully started saving data"}, safe=False)


def data_saving_task(
    aas_collection_name: str = "aas_collection",
    submodel_collection_name: str = "submodel_collection",
):
    for collection, url in (
        (aas_collection_name, settings.AAS_URL),
        (submodel_collection_name, settings.SUBMODELS_URL),
    ):
        collection = get_or_create_database_collection(
            database_name=settings.MONGO_DATABASE_NAME, collection_name=collection
        )
        insert_document_in_collection(collection, url)

    logging.debug(f"{collection}, Data has been saved at: {datetime.datetime.now()}")
