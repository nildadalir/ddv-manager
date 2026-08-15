from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.session import get_database
from backend.database.models import Item, ItemCategory
from backend.schemas.item import ItemResponse


router = APIRouter(
    prefix="/items",
    tags=["items"],
)


def build_item_response(item: Item) -> ItemResponse:
    return ItemResponse(
        name=item.name,
        category=item.category.name if item.category else None,
        rarity=item.rarity,
        sell_price=item.sell_price,
    )


@router.get("/", response_model=list[ItemResponse])
def get_items(
    db: Session = Depends(get_database),
):
    items = (
        db.query(Item)
        .join(ItemCategory)
        .all()
    )

    return [
        build_item_response(item)
        for item in items
    ]


@router.get("/search", response_model=list[ItemResponse])
def search_items(
    name: str,
    db: Session = Depends(get_database),
):
    items = db.query(Item).filter(
        Item.name.ilike(f"%{name}%")
    ).all()

    return [
        build_item_response(item)
        for item in items
    ]


@router.get("/{item_id}/recipes")
def get_item_recipes(
    item_id: int,
    db: Session = Depends(get_database),
):
    item = db.query(Item).filter(
        Item.item_id == item_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )

    return [
        {
            "name": link.recipe.name,
            "category": link.recipe.category,
            "stars": link.recipe.stars,
            "quantity": link.quantity,
        }
        for link in item.recipe_links
    ]