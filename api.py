from flask import jsonify
import azure.functions as func
from pymongo import MongoClient
import os

app = func.FunctionApp()

# Azure Cosmos DB for MongoDB connection string
COSMOS_DB_URI = os.getenv('CONNECTION_STRING')
DATABASE_NAME = 'dcis'

# MongoDB client initialization
client = MongoClient(COSMOS_DB_URI)
db = client[DATABASE_NAME]

@app.route(route="enclosures", auth_level=func.AuthLevel.ANONYMOUS, methods=['GET'])
def fetchEnclosure(req: func.HttpRequest) -> func.HttpResponse:
    try:
        tag = req.params.get('tag')
        
        collection = db['situations']
        query = {'tag':tag}
        data = collection.find_one(query)
        del data['_id']
        
        return func.HttpResponse(jsonify(data),status_code=200)
    except Exception as e:
        return func.HttpResponse(jsonify({"error": str(e)}), 500)
