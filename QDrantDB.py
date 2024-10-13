from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, models, ScoredPoint,Record

CLIENT = QdrantClient(host="localhost", port=6333)
OBJECTCOLLECTION = "PyWorkBenchObjects"


if not CLIENT.collection_exists(OBJECTCOLLECTION):
   CLIENT.create_collection(
      collection_name=OBJECTCOLLECTION,
      vectors_config=VectorParams(size=100, distance=Distance.COSINE),
   )

def createNewObject(obj) -> int:
    response = CLIENT.upsert(
        collection_name=OBJECTCOLLECTION,
        points=[
            models.PointStruct(
                payload=obj
            )
        ]
    )
    return response[0].id

def getObject(id: int):
    return CLIENT.retrieve(
        collection_name=OBJECTCOLLECTION,
        ids=[id]
    )[0].payload

def setObjectVector(id: int, vector: list[float]):
    CLIENT.upsert(
        collection_name=OBJECTCOLLECTION,
        points=[
            models.PointStruct(
                id=id,
                vector=vector
            )
        ]
    )

def getCloseObjects(vector: list[float]) -> list[ScoredPoint]:
    return CLIENT.search(
    collection_name="my_collection",
    query_vector=vector,
    limit=5  # Return 5 closest points
    )