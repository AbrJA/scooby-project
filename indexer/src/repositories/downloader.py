import gdown
import logging
import zipfile

from src.config import Configuration

class Downloader:
    """
    A class to download files from a public Google Drive URL.
    """
    def __init__(self):
        """
        Initializes the downloader with the file URL and output path.
        """
        config = Configuration()
        self.url = config.Downloader.url
        self.path = config.Downloader.path

    def get_files(self):
        """
        Executes the file download from the specified Google Drive URL.
        """
        logging.info("Downloading file...")
        try:
            gdown.download(self.url, self.path, quiet=False, fuzzy=True)
            with zipfile.ZipFile(self.path, 'r') as file:
                file.extractall()
            # logging.info("File successfully downloaded to: %s", self.path)
        except Exception as e:
            logging.error("An error occurred during download: %s", e)
