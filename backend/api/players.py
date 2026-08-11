from fastapi import APIRouter, Depends, HTTPException
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
    PlayerCharacterUpdate,
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


@router.patch("/{player_id}/characters/{character_id}")
def update_character(
    player_id: int,
    character_id: int,
    data: PlayerCharacterUpdate,
    db: Session = Depends(get_database)
):
    print("PATCH DATA:", data.model_dump())

    player_character = db.query(PlayerCharacter).filter(
        PlayerCharacter.player_id == player_id,
        PlayerCharacter.character_id == character_id
    ).first()

    if not player_character:
        raise HTTPException(
            status_code=404,
            detail="Character not found for this player"
        )

    if data.unlocked is not None:
        player_character.unlocked = data.unlocked

    if data.friendship_level is not None:
        player_character.friendship_level = data.friendship_level

    if data.role_id is not None:
        player_character.assigned_role = data.role_id

    print(
        "BEFORE COMMIT:",
        player_character.assigned_role,
        player_character.friendship_level,
        player_character.unlocked
    )

    db.commit()
    db.refresh(player_character)

    return {
        "message": "Character updated",
        "character_id": player_character.character_id,
        "unlocked": player_character.unlocked,
        "friendship_level": player_character.friendship_level,
        "role_id": player_character.assigned_role
    }