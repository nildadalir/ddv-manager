from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_database
from backend.database.models import Character, Franchise
from backend.schemas.character import CharacterResponse


router = APIRouter(
    prefix="/characters",
    tags=["characters"],
)


def build_character_response(character: Character) -> CharacterResponse:
    return CharacterResponse(
        name=character.name,
        species=character.species,
        franchise=character.franchise.name if character.franchise else None,
    )


@router.get("/", response_model=list[CharacterResponse])
def get_characters(
    db: Session = Depends(get_database),
):
    characters = (
        db.query(Character)
        .join(Franchise)
        .all()
    )

    return [
        build_character_response(character)
        for character in characters
    ]


@router.get("/search", response_model=list[CharacterResponse])
def search_characters(
    name: str,
    db: Session = Depends(get_database),
):
    characters = db.query(Character).filter(
        Character.name.ilike(f"%{name}%")
    ).all()

    return [
        build_character_response(character)
        for character in characters
    ]