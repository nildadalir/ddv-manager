from pydantic import BaseModel


class IngredientResponse(BaseModel):
    name: str
    quantity: int


class RecipeResponse(BaseModel):
    name: str
    category: str | None
    stars: int | None
    ingredients: list[IngredientResponse]