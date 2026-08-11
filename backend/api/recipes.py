from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_database
from backend.database.models import Recipe
from backend.schemas.recipe import (
    RecipeResponse,
    IngredientResponse
)


router = APIRouter(
    prefix="/recipes",
    tags=["recipes"]
)


@router.get("/", response_model=list[RecipeResponse])
def get_recipes(
    db: Session = Depends(get_database)
):

    recipes = db.query(Recipe).all()

    return [
    RecipeResponse(
        name=recipe.name,
        category=recipe.category,
        stars=recipe.stars,
        ingredients=[
            IngredientResponse(
                name=ingredient.item.name,
                quantity=ingredient.quantity
            )
            for ingredient in recipe.ingredients
        ]
    )
    for recipe in recipes
]