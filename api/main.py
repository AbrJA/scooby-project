import uvicorn
from repositories.qdrant import Qdrant
from repositories.embedder import Embedder
from fastapi import FastAPI, UploadFile, File, Form
from starlette.responses import JSONResponse

app = FastAPI(title="Multimodal search")
qdrant = Qdrant()
qdrant.create_client()
embedder = Embedder()
embedder.load_model()

# TODO: change id to petid
@app.post("/search",
    summary="Search for similar items",
    description="""
    Searches the Qdrant database for similar items based on one of three input types:
    - **`id`**: Finds the item with the specified point ID and retrieves similar items.
    - **`text`**: Embeds the provided text query and searches for the most similar items.
    - **`image`**: Embeds the uploaded image and searches for the most similar items.

    Exactly one of these fields must be provided.
    """,)
async def search(
    id: int | None = Form(
        None,
        description="A specific point ID to search for (e.g., to find similar pets to a known one). Mutually exclusive with `text` and `image`."
    ),
    text: str | None = Form(
        None,
        description="A text query (e.g., 'a fluffy golden retriever') to find similar items. Mutually exclusive with `id` and `image`."
    ),
    image: UploadFile | None = File(
        None,
        description="An image file to use for finding similar items. Mutually exclusive with `id` and `text`."
    ),
    limit: int = Form(
        5,
        ge=1,
        description="The maximum number of similar items to return."
    ),
):
    """
    Handles the search logic based on the provided input.
    """
    if id is not None:
        return qdrant.search_point(id, limit)
    elif text is not None:
        vector = embedder.project_text(text)
        return qdrant.search_point(vector.flatten(), limit)
    elif image is not None:
        img_bytes = await image.read()
        vector = embedder.project_image(img_bytes)
        return qdrant.search_point(vector.flatten(), limit)
    else:
        return JSONResponse(content={"error": "No id, text, or image provided"}, status_code=400)

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
