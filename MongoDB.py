from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

client: MongoClient = MongoClient("mongodb://localhost:27017/")
WorkBenchDB: Database = client["PyWorkBench"]
Objects: Collection = WorkBenchDB["Objects"]

def createNewObject(obj: object) -> str:
    return Objects.insert_one({"_obj": to_dict(obj)}).inserted_id

def updateObject(id: str, obj: object):
    objdict = to_dict(obj)
    Objects.update_one({"_id": id}, {"$set": {"_obj": objdict}})

def getObject(id: str) -> object:
    return from_dict(Objects.find_one({"_id": id})["_obj"]) #type: ignore


def to_dict(obj):
    """
    Recursively convert an object to a dictionary, including nested objects.
    """
    if isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    elif hasattr(obj, "__dict__"):
        # Handle objects by converting their __dict__
        return {k: to_dict(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, list):
        # Convert lists recursively
        return [to_dict(i) for i in obj]
    else:
        return obj  # Return basic data types directly

def from_dict(data, cls):
    """
    Recursively convert a dictionary back to an object of the given class.
    Assumes the dictionary keys match the attributes of the class.
    """
    if isinstance(data, dict):
        kwargs = {}
        for key, value in data.items():
            attr_type = getattr(cls, key, None)
            # Handle nested objects
            if isinstance(value, dict) and attr_type:
                kwargs[key] = from_dict(value, attr_type.__class__)
            else:
                kwargs[key] = value
        return cls(**kwargs)
    return data
class SubObject:
    sub_val: int
    def __init__(self, sub_val):
        self.sub_val = sub_val

createNewObject({"test": "test",
        "list": [SubObject(1),SubObject(2), SubObject(3)],
        "dict": {"key1": "value1", "key2": "value2"}})