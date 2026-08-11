from fastapi import FastAPI

from backend.api.characters import router as character_router
from backend.api.items import router as item_router
from backend.api.recipes import router as recipe_router


app = FastAPI(
    title="DDV Manager API"
)


app.include_router(character_router)
app.include_router(item_router)
app.include_router(recipe_router)


@app.get("/")
def root():
    return {
        "message": "DDV Manager API running"
    }
    