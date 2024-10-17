from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import pickle

client: MongoClient = MongoClient("mongodb://localhost:27017/")
WorkBenchDB: Database = client["PyWorkBench"]
Objects: Collection = WorkBenchDB["Objects"]

def createNewObject(obj: object) -> str:
    return Objects.insert_one({"_obj": pickle.dumps(obj)}).inserted_id

def updateObject(id: str, obj: object):
    objdict = pickle.dumps(obj)
    Objects.update_one({"_id": id}, {"$set": {"_obj": objdict}})

def getObject(id: str) -> object:
    return pickle.loads(Objects.find_one({"_id": id})["_obj"]) #type: ignore