import uvicorn
from repositories.qdrant import Qdrant
from repositories.embedder import Embedder
from fastapi import FastAPI, UploadFile, File, Form
from starlette.responses import JSONResponse

app = FastAPI(title="Qdrant API")
qdrant = Qdrant()
qdrant.create_client()
embedder = Embedder()
embedder.load_model()

# TODO: change id to petid
@app.post("/search")
async def search(
    id: int | None = Form(None),
    text: str | None = Form(None),
    image: UploadFile | None = File(None),
    limit: int = Form(5),
):
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
