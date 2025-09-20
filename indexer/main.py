import logging
from repositories.qdrant import Qdrant
from repositories.embedder import Embedder
from repositories.downloader import Downloader
from indexer import Indexer
def main():
    downloader = Downloader()
    embedder = Embedder()
    qdrant = Qdrant()
    indexer = Indexer(downloader, qdrant, embedder)
    indexer.run_indexing('./images', './images/information.csv')

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logging.getLogger('httpx').setLevel(logging.WARNING)

    main()
