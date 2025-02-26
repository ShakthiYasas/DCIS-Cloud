from flask import Flask, jsonify, request
from pymongo import MongoClient
import os

app = Flask(__name__)

# Azure Cosmos DB for MongoDB connection string
COSMOS_DB_URI = "mongodb://dcisdatabase:9kgbdJI0IlhqrSD7x5gtRoQTeYpE2ZCDEjndYXfz85P2b8iGxMvMsiiSJlv3IqiQLVsS1lait0eZACDbyq6B4A==@dcisdatabase.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@dcisdatabase@"
DATABASE_NAME = 'dcis'

# MongoDB client initialization
client = MongoClient(COSMOS_DB_URI)
db = client[DATABASE_NAME]

@app.route('/enclosures', methods=['GET'])
def getEnclosureMetaData():
    try:
        # Retrieving the data from the situations collection.
        collection = db['situations']
        args = request.args
        if(len(args)>0):
            # Retrieving the enclosure tag.
            tag = args['tag']
            query = {'tag':tag}
            data = collection.find_one(query)
            del data['_id']
            print(data)

            return jsonify(data), 200
        else:
            # Retrieving all the enclosures
            data = list(collection.find({}, {'_id':0}))

            return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)