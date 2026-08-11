from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.database.session import get_database
from backend.database.models import (
    Player,
    PlayerCharacter,
)

from backend.schemas.player import (
    PlayerResponse,
    PlayerCharacterResponse,
    PlayerCharacterCreate,
)


router = APIRouter(
    prefix="/players",
    tags=["players"]
)


@router.get("/", response_model=list[PlayerResponse])
def get_players(
    db: Session = Depends(get_database)
):

    players = db.query(Player).all()

    return [
        PlayerResponse(
            username=player.username,
            characters=[
                PlayerCharacterResponse(
                    name=pc.character.name,
                    unlocked=pc.unlocked,
                    friendship_level=pc.friendship_level,
                    role=pc.role.name if pc.role else None
                )
                for pc in player.characters
            ]
        )
        for player in players
    ]


@router.post("/{player_id}/characters")
def add_character(
    player_id: int,
    data: PlayerCharacterCreate,
    db: Session = Depends(get_database)
):

    existing = db.query(PlayerCharacter).filter(
        PlayerCharacter.player_id == player_id,
        PlayerCharacter.character_id == data.character_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Character already added to player"
        )

    player_character = PlayerCharacter(
        player_id=player_id,
        character_id=data.character_id,
        unlocked=data.unlocked,
        friendship_level=data.friendship_level,
        assigned_role=data.role_id
    )

    db.add(player_character)
    db.commit()
    db.refresh(player_character)

    return {
        "message": "Character added",
        "character_id": player_character.character_id
    }