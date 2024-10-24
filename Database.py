from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import dill #type: ignore # extended pickle functionality

client: MongoClient = MongoClient("mongodb://localhost:27017/")
WorkBenchDB: Database = client["PyWorkBench"]
Objects: Collection = WorkBenchDB["Objects"]

def createNewObject(obj: object) -> str:
    return Objects.insert_one({"_obj": dill.dumps(obj)}).inserted_id

def updateObject(id: str, obj: object):
    Objects.update_one({"_id": id}, {"$set": {"_obj": dill.dumps(obj)}})

def getObject(id: str) -> object:
    return dill.loads(Objects.find_one({"_id": id})["_obj"]) #type: ignore
    # pickle.loads can have issues when required packages aren't loaded

def deleteObject(id: str):
    Objects.delete_one({"_id": id})

def clearOrphans(RootId: str):
    """!!!Danger!!!
    Deletes all objects that are not reachable from the root object.
    Use with care!"""
    #TODO clear orphans
    raise NotImplementedError