from fastapi import FastAPI

from backend.api.characters import router as character_router
from backend.api.items import router as item_router
from backend.api.recipes import router as recipe_router
from backend.api.players import router as player_router
from backend.api.role_preferences import router as role_preferences_router


app = FastAPI(
    title="DDV Manager API"
)


app.include_router(character_router)
app.include_router(item_router)
app.include_router(recipe_router)
app.include_router(player_router)
app.include_router(role_preferences_router)


@app.get("/")
def root():
    return {
        "message": "DDV Manager API running"
    }