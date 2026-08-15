from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.session import get_database
from backend.database.models import Recipe
from backend.schemas.recipe import (
    RecipeResponse,
    IngredientResponse,
)


router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
)


def build_recipe_response(recipe: Recipe) -> RecipeResponse:
    return RecipeResponse(
        name=recipe.name,
        category=recipe.category,
        stars=recipe.stars,
        ingredients=[
            IngredientResponse(
                name=ingredient.item.name,
                quantity=ingredient.quantity,
            )
            for ingredient in recipe.ingredients
        ],
    )


@router.get("/", response_model=list[RecipeResponse])
def get_recipes(
    db: Session = Depends(get_database),
):
    recipes = db.query(Recipe).all()

    return [
        build_recipe_response(recipe)
        for recipe in recipes
    ]


@router.get("/search", response_model=list[RecipeResponse])
def search_recipes(
    name: str,
    db: Session = Depends(get_database),
):
    recipes = db.query(Recipe).filter(
        Recipe.name.ilike(f"%{name}%")
    ).all()

    return [
        build_recipe_response(recipe)
        for recipe in recipes
    ]


@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_database),
):
    recipe = db.query(Recipe).filter(
        Recipe.recipe_id == recipe_id
    ).first()

    if not recipe:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found",
        )

    return build_recipe_response(recipe)