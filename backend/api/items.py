from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_database
from backend.database.models import Item, ItemCategory


router = APIRouter(
    prefix="/items",
    tags=["items"]
)


@router.get("/")
def get_items(
    db: Session = Depends(get_database)
):

    items = (
        db.query(Item)
        .join(ItemCategory)
        .all()
    )

    return [
        {
            "name": item.name,
            "category": item.category.name,
            "rarity": item.rarity,
            "sell_price": item.sell_price
        }
        for item in items
    ]
    