import logging

from src.config import Configuration
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct

class Qdrant():
    def __init__(self):
        config = Configuration()
        self.url = config.Qdrant.url
        self.port = config.Qdrant.port
        self.collection = config.Qdrant.collection
        self.distance = Distance.COSINE
        self.size = config.Embedder.size
        # self.timeout = config.Qdrant.timeout

    def create_client(self):
        """
        Creates a Qdrant client.
        """
        logging.info("Creating Qdrant client...")
        try:
            self.client = QdrantClient(host=self.url, port=self.port)
        except Exception as e:
            logging.error("An error occurred during client creation: %s", e)

    def create_collection(self):
        """
        Creates a Qdrant collection.
        """
        if not self.client.collection_exists(collection_name=self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=self.size, distance=self.distance)
            )

    def upsert_point(self, id, vector, payload):
        """
        Upserts a point into the Qdrant collection.
        Args:
            id (int): The id of the point.
            vector (list): The vector of the point.
            payload (dict): The payload of the point.
        """
        self.client.upsert(
            collection_name=self.collection,
            points=[
                PointStruct(
                    id=id,
                    vector=vector,
                    payload=payload
                )
            ]
        )
