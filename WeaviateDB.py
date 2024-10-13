import weaviate
from weaviate.classes.init import AdditionalConfig, Timeout
import os

# Connect to Weaviate
client = weaviate.connect_to_local(
    port=8080,
    grpc_port=50051,
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120)  # Values in seconds
    ),
    skip_init_checks=True
)

client.connect()

# Check if the server is live
def is_live()-> bool:
    return client.is_live()


# def createNewObject(obj):

# def getObject(id: int):

# def setObjectVector(id: int, vector: list[float]):

# def getCloseObjects(vector: list[float]) -> list[ScoredPoint]: