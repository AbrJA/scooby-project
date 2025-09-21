import logging

from config import Configuration
from PIL import Image
from uform import get_model, Modality
from io import BytesIO

class Embedder:
    def __init__(self):
        config = Configuration()
        self.name = config.Embedder.name

    def load_model(self):
        """
        Loads the image and text encoders from the specified model name.
        """
        logging.info("Loading embedder...")
        try:
            processors, models = get_model(self.name)
            self.model_image = models[Modality.IMAGE_ENCODER]
            self.processor_image = processors[Modality.IMAGE_ENCODER]
            self.model_text = models[Modality.TEXT_ENCODER]
            self.processor_text = processors[Modality.TEXT_ENCODER]
        except Exception as e:
            logging.error("An error occurred during model loading: %s", e)

    def project_image(self, bytes: bytes):
        """
        Processes an image, encodes it, and returns the encoded vector.
        Args:
            image (Image): The image to process.
        Returns:
            The encoded vector of the image.
        """
        image = Image.open(BytesIO(bytes))#.convert("RGB")
        processed_image = self.processor_image(image)
        return self.model_image.encode(processed_image, return_features=False)

    def project_text(self, text: str):
        """
        Processes a text query, encodes it, and returns the encoded vector.
        Args:
            text (str): The text query to process.
        Returns:
            The search results from the index.
        """
        processed_text = self.processor_text(text)
        return self.model_text.encode(processed_text, return_features=False)
