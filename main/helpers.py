import requests
import logging

from django.conf import settings
from pymongo import MongoClient


def connect_database() -> MongoClient:
    return MongoClient(settings.MONGO_URL)


def get_or_create_database(database_name: str):
    client = connect_database()
    return client[database_name]


def get_or_create_database_collection(
    database_name: str = "aas_database", collection_name: str = "aas_collection"
):
    db = get_or_create_database(database_name)
    collection = db[collection_name]
    return collection


def insert_document_in_collection(
    collection,
    url: str = "http://mes_aas:5111/aas",
):
    try:
        response = requests.get(url, headers={"Content-Type": "application/json"})
        if response.status_code // 100 == 2:
            logging.debug(
                f"Request to Server for fetching AAS/SUBMODELS, request successful: {response.text}"
            )
            document = response.json()
            if "submodel" in url:
                for submodel in document:
                    update_or_create_document(collection, submodel)
            else:
                update_or_create_document(collection, document)
        else:
            logging.error(
                f"Request to Server for fetching AAS/SUBMODELS, request failed with status code: {response.status_code}"
            )
    except (requests.exceptions.RequestException, requests.ConnectionError) as error:
        logging.error(
            f"Request to Server for fetching AAS/SUBMODELS, request failed with error : {error}"
        )


def update_or_create_document(collection, document: dict):
    document_id = document.get("identification")["id"]
    if existing_document := collection.find_one({"_id": document_id}):
        collection.update_one({"_id": document_id}, {"$set": document})
    else:
        document = {"_id": document_id} | document
        collection.insert_one(document)
