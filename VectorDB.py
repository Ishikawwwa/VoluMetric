from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os
from dotenv import load_dotenv

class VectorDB:
     
    def __init__(self):
        load_dotenv()
        self.client = QdrantClient(
            url=os.getenv("VECTOR_DB_URL"), 
            api_key=os.getenv("VECTOR_DB_API"),
        )

    def createCollection(self, collection_name, vector_size):
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.EUCLID),
        )

    def deleteCollection(self, collection_name):
        self.client.delete_collection(
            collection_name=collection_name,
        )
    
    def addVector(self, collection_name, embedding, i):
        operation_info = self.client.upsert(
            collection_name=collection_name,
            wait=True,
            points=[
                PointStruct(id=i, vector=embedding),
            ],
        )
        print(operation_info)

    def searchNearest(self, collection_name, embedding):
        search_result = self.client.search(
            collection_name=collection_name, query_vector=embedding, limit=3
        )
        result = self.client.retrieve(collection_name=collection_name, ids=[search_result[0].id, search_result[1].id, search_result[2].id], with_vectors=True)

        return result