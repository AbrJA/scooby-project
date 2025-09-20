import os

class Configuration:
    def __init__(self):
        self.Downloader = Downloader()
        self.Embedder = Embedder()
        self.Qdrant = Qdrant()

class Downloader:
    def __init__(self):
        self.url = os.environ.get('DOWNLOADER_URL')
        self.path = os.environ.get('DOWNLOADER_PATH')

class Embedder:
    def __init__(self):
        self.name = os.environ.get('EMBEDDER_NAME')
        self.size = int(os.environ.get('EMBEDDER_SIZE'))

class Qdrant:
    def __init__(self):
        self.url = os.environ.get('QDRANT_URL')
        self.port = int(os.environ.get('QDRANT_PORT'))
        self.collection = os.environ.get('QDRANT_COLLECTION')
        # self.timeout = int(os.environ.get('QDRANT_TIMEOUT'))
        # self.api_key = os.environ.get('QDRANT_API_KEY')
