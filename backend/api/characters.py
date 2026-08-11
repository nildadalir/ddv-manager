from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_database
from backend.database.models import Character, Franchise


router = APIRouter(
    prefix="/characters",
    tags=["characters"]
)


@router.get("/")
def get_characters(
    db: Session = Depends(get_database)
):

    characters = (
        db.query(Character)
        .join(Franchise)
        .all()
    )

    return [
        {
            "name": character.name,
            "species": character.species,
            "franchise": character.franchise.name
        }
        for character in characters
    ]