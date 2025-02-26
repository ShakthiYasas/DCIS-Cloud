from fastapi import FastAPI
from pymongo import MongoClient
import os

app = FastAPI()

# Azure Cosmos DB for MongoDB connection string
COSMOS_DB_URI = "mongodb://dcisdatabase:9kgbdJI0IlhqrSD7x5gtRoQTeYpE2ZCDEjndYXfz85P2b8iGxMvMsiiSJlv3IqiQLVsS1lait0eZACDbyq6B4A==@dcisdatabase.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@dcisdatabase@"
DATABASE_NAME = 'dcis'

# MongoDB client initialization
client = MongoClient(COSMOS_DB_URI)
db = client[DATABASE_NAME]

@app.get('/enclosures')
async def getEnclosureMetaData(tag: str):
    try:
        # Retrieving the data from the situations collection.
        collection = db['situations']
        query = {'tag':tag}
        data = collection.find_one(query)
        del data['_id']

        return data, 200
    except Exception as e:
        return {"error": str(e)}, 500
