from pymongo import MongoClient, DESCENDING
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import string
import time  
import os

app = FastAPI()

length = 8

# Azure Cosmos DB for MongoDB connection string
COSMOS_DB_URI = os.environ['CONNECTION_STRING']
DATABASE_NAME = 'dcis'

# MongoDB client initialization
client = MongoClient(COSMOS_DB_URI)
db = client[DATABASE_NAME]

@app.get('/enclosures', status_code=200)
async def getEnclosureMetaData(tag: str):
        # Retrieving the data from the situations collection.
        collection = db['situations']
        query = {'tag':tag}
        data = collection.find_one(query)

        if data is None:
            raise HTTPException(400, 'Invalid enclosure tag.')

        del data['_id']
        data['session'] = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        return data

@app.get('/backups', status_code=200)
async def getContextBackup(tag: str):
    collection = db['contextBackup']
    query = {'enclosure':tag}
    data = collection.find_one(query, sort=[('timestamp', DESCENDING)])
    
    if data is None:
        raise HTTPException(400, f'{tag} is an invalid enclosure tag.')
    
    del data['_id']
    
    current_time = int(time.time())
    if((current_time - data['timestamp']) > 1800000):
        raise HTTPException(404, 'Backup context is stale!')
    
    del data['timestamp']

    return data

@app.get('/situations', status_code=200)
async def getSituationDescription(name: str):
    collection = db['predefinedSituations']
    query = {'situationName':name}
    data = collection.find_one(query)
    
    if data is None:
        raise HTTPException(400, f'No situation description by the name {name}.')
    
    del data['_id']
    return data

class Log(BaseModel):
    message: str

@app.post('/logs', status_code=201)
async def createLog(log: Log):
    try:
        collection = db['logs']
        data = dict()
        data['message'] = log.message
        collection.insert_one(data)

        return {'message': 'Logging successful.'}
    except Exception as e:
        raise HTTPException(500, f'{str(e)} An error occured when creating the log.')
    
class Context(BaseModel):
    enclosure: str
    context: float

@app.post('/backups', status_code=201)
async def createBackup(context: Context):
    try:
        collection = db['contextBackup']
        data = dict() 
        data['enclosure'] = context.enclosure
        data['context'] = context.context
        data['timestamp'] = int(time.time())
        collection.insert_one(data)

        return {'message': 'Backup successful.'}
    except Exception:
        raise HTTPException(500, 'An error occured when creating the log.')