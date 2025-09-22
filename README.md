# Scooby Project

# Multimodal Search with Qdrant and UFORM

This project implements a multimodal search engine that allows you to find similar images based on a text query or another image. It uses a combination of Qdrant as a vector database, UFORM for generating embeddings, and FastAPI to provide a REST API.

---

## 🚀 Key Features

* **Multimodal Search**: Search for images using either a text description or a reference image.
* **Vector Database**: Utilizes Qdrant for efficient storage and similarity search of high-dimensional vectors.
* **State-of-the-Art Embeddings**: Uses the `unum-cloud/uform3-image-text-english-small` model to create robust image and text embeddings.
* **Scalable Architecture**: The project is containerized using Docker Compose, allowing for easy deployment and scaling of each component.
* **REST API**: A simple and clean API built with FastAPI for querying the search engine.
* **Automatic Indexing**: An indexer service automatically downloads and processes a dataset, populating the vector database.

---

## 🗺️ Architecture

The project consists of three main services, all orchestrated by Docker Compose:

1.  **`qdrant`**: The core vector database responsible for storing the high-dimensional vectors and performing efficient similarity searches. It exposes ports `6333` (gRPC) and `6334` (HTTP) for communication.
2.  **`indexer`**: A service that handles the data preparation. It downloads a dataset (e.g., a `.zip` file of images and captions), uses the UFORM model to generate embeddings, and indexes them into the `qdrant` collection.
3.  **`api`**: A FastAPI application that serves as the public interface for the search engine. It accepts search queries (text or image), generates embeddings on the fly, and uses the Qdrant client to perform a nearest-neighbor search.

```
+----------------+          +-----------------+
|   qdrant       | <--------|     indexer     |
| (Vector DB)    |          |   (Data Prep)   |
+----------------+          +-----------------+
        ^                            ^
        |                            |
        |                            |
+----------------+          +-----------------+
|    api         | <--------|   frontend      |
| (FastAPI)      |          |   (UI) TO DO    |
+----------------+          +-----------------+
```

## 🔧 Setup & Installation

### Prerequisites

* [Docker](https://www.docker.com/get-started)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Steps

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/AbrJA/scooby-project
    cd scooby-project
    ```

2.  **Configure Environment Variables (Optional)**:
    Your Docker Compose file is pre-configured, but you can adjust environment variables within the `docker-compose.yml` if needed, for example, to point to a different dataset or change the collection name.

3.  **Build and Run with Docker Compose**:
    This command will build the necessary images, create the network, and start all services in detached mode.

    ```bash
    docker-compose up --build -d
    ```
    * The `qdrant` container will start and perform a health check to ensure it's ready.
    * The `indexer` will wait for `qdrant` to be healthy, then start its indexing process. This may take some time depending on the dataset size. You can view its progress with `docker-compose logs indexer`.
    * The `api` service will also wait for `qdrant` to be available before starting.

4.  **Verify Services**:
    You can check the status of your containers to ensure they are all running as expected.
    ```bash
    docker-compose ps
    ```
    You should see `qdrant` with a status of `healthy`, and `api` and `indexer` with a status of `up`.

---

## 👩‍💻 Usage

Once all services are running, the API is available at `http://localhost:8000`.

### API Documentation

The FastAPI service automatically generates interactive API documentation. You can access it in your browser:

* **Swagger UI**: `http://localhost:8000/docs`
* **ReDoc**: `http://localhost:8000/redoc`

### The `/search` Endpoint

The API has a single, flexible search endpoint that accepts a query as either a `text` string, an `image` file, or a Qdrant point `id`.

* **Endpoint**: `POST /search`
* **Method**: `POST`
* **Content Type**: `multipart/form-data`

#### Parameters

The endpoint requires **exactly one** of the following parameters to be provided in the form data:

| Parameter | Type | Description |
| :--- | :--- | :--- |
| **`id`** | `int` | (Optional) The specific point ID to search for (e.g., to find similar items to a known one). |
| **`text`** | `str` | (Optional) A text query (e.g., "a fluffy golden retriever") to find similar items. |
| **`image`** | `file` | (Optional) An image file to use for finding similar items. |
| **`limit`** | `int` | The maximum number of similar items to return. (Default: 5) |

#### Example Usage

**1. Search with a Text Query**

To search using text, provide the `text` parameter in your request body.

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: multipart/form-data" \
  -F "text=A black cat with a funny hat"
```

**2. Search with an Image**

To search with an image, provide the image file.

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@/path/to/your/image.jpg"
```
(Replace /path/to/your/image.jpg with the actual path to your image file.)

**3. Search by ID**

To find items similar to a specific item already in the database, provide its id.

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: multipart/form-data" \
  -F "id=123"
```

## 🌐 UI Setup & Access (TO DO)

## 🛑 Stopping the Services

To stop and remove all containers, networks, and volumes created by `docker-compose up`, run:

```bash
docker-compose down
```

## 📂 Project Structure

```
.
├── api/                  # FastAPI application
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── indexer/              # Indexing service
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── storage/              # Persistent storage for Qdrant data
├── .gitignore
├── docker-compose.yml
└── README.md             # This file
```
