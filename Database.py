from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import dill #type: ignore # extended pickle functionality

def getCollection() -> Collection:
    client: MongoClient = MongoClient("mongodb://localhost:27017/")
    WorkBenchDB: Database = client["PyWorkBench"]
    return WorkBenchDB["Objects"]

def createNewObject(obj: object) -> str:
    return getCollection().insert_one({"_obj": dill.dumps(obj)}).inserted_id

def updateObject(id: str, obj: object):
    getCollection().update_one({"_id": id}, {"$set": {"_obj": dill.dumps(obj)}})

def getObject(id: str) -> object:
    return dill.loads(getCollection().find_one({"_id": id})["_obj"]) #type: ignore
    # pickle.loads can have issues when required packages aren't loaded

def deleteObject(id: str):
    getCollection().delete_one({"_id": id})