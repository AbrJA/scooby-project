import logging

from config import Configuration
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

    def search_point(self, query, limit=5):
        return self.client.query_points(
            collection_name=self.collection,
            query=query,
            limit=limit
        )
