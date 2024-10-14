import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
dbName = "PyWorkBench"
objectsName = "Objects"

WorkBenchDB = myclient[dbName]
Objects = WorkBenchDB[objectsName]

def createNewObject(obj) -> str:
    return Objects.insert_one(obj).inserted_id

def getObject(id: str):
    return Objects.find_one({"_id": id})