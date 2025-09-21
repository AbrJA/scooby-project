import os

class Configuration:
    def __init__(self):
        self.Embedder = Embedder()
        self.Qdrant = Qdrant()

class Embedder:
    def __init__(self):
        self.name = os.environ.get('EMBEDDER_NAME')
        self.size = int(os.environ.get('EMBEDDER_SIZE'))

class Qdrant:
    def __init__(self):
        self.url = os.environ.get('QDRANT_URL')
        self.port = int(os.environ.get('QDRANT_PORT'))
        self.collection = os.environ.get('QDRANT_COLLECTION')
