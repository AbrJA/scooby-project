FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

ENV QDRANT_URL=localhost \
    QDRANT_PORT=6333 \
    QDRANT_COLLECTION=adoption1 \
    EMBEDDER_NAME=unum-cloud/uform3-image-text-english-small \
    EMBEDDER_SIZE=256 \
    DOWNLOADER_URL=https://drive.google.com/uc?id=1pG0eI1cczWfgLs5L47SkVzmpXkoZ0Uc9 \
    DOWNLOADER_PATH=adoption.zip

COPY src/ src/
COPY main.py .

CMD ["python", "main.py"]
