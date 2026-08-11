from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_database
from backend.database.models import Item, ItemCategory
from backend.schemas.item import ItemResponse


router = APIRouter(
    prefix="/items",
    tags=["items"]
)


@router.get("/", response_model=list[ItemResponse])
def get_items(
    db: Session = Depends(get_database)
):

    items = (
        db.query(Item)
        .join(ItemCategory)
        .all()
    )

    return [
    ItemResponse(
        name=item.name,
        category=item.category.name if item.category else None,
        rarity=item.rarity,
        sell_price=item.sell_price
    )
    for item in items
]