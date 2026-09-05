from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.characters import router as character_router
from backend.api.items import router as item_router
from backend.api.recipes import router as recipe_router
from backend.api.players import router as player_router
from backend.api.role_preferences import router as role_preferences_router
from backend.api.home import router as home_router
from backend.api.activity_roles import router as activity_roles_router


app = FastAPI(
    title="DDV Manager API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(character_router)
app.include_router(item_router)
app.include_router(recipe_router)
app.include_router(player_router)
app.include_router(role_preferences_router)
app.include_router(home_router)
app.include_router(activity_roles_router)


@app.get("/")
def root():
    return {
        "message": "DDV Manager API running"
    }