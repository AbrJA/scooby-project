import os
import logging
import pandas as pd
from PIL import Image

class Indexer:
    def __init__(self, downloader, qdrant, embedder):
        self.downloader = downloader
        self.qdrant = qdrant
        self.embedder = embedder

    """
    Run the indexing process.
    """
    def run_indexing(self, dir_images, file_csv):
        # 1. Download files
        self.downloader.get_files()
        # 2. Set up Qdrant
        self.qdrant.create_client()
        self.qdrant.create_collection()
        # 3. Load embedder model
        self.embedder.load_model()
        # 4. Ingest data
        information = pd.read_csv(file_csv)
        image_files = [f for f in os.listdir(dir_images) if f.endswith('.jpg')]

        image_files = image_files[0:10]
        total_images = len(image_files)

        for i, path in enumerate(image_files):
            image = Image.open(os.path.join(dir_images, path))
            vector = self.embedder.project_image(image)
            pet_id = os.path.splitext(os.path.basename(path))[0]
            payload = information[information['petid'] == pet_id].iloc[0].to_dict()
            self.qdrant.upsert_point(i, vector.flatten(), payload)
            if i % 100 == 0:
                logging.info(f'Ingested {i}/{total_images} vectors into collection')
