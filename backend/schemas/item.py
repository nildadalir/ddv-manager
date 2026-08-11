from pydantic import BaseModel


class ItemResponse(BaseModel):
    name: str
    category: str | None
    rarity: str | None
    sell_price: int | None