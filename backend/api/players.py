from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.session import get_database
from backend.database.models import (
    Player,
    PlayerCharacter,
    Character,
    Role,
)
from backend.schemas.player import (
    PlayerResponse,
    PlayerCharacterResponse,
    PlayerCharacterCreate,
    PlayerCharacterUpdate,
)


router = APIRouter(
    prefix="/players",
    tags=["players"],
)


@router.get("/", response_model=list[PlayerResponse])
def get_players(
    db: Session = Depends(get_database),
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
                    role=pc.role.name if pc.role else None,
                )
                for pc in player.characters
            ],
        )
        for player in players
    ]


@router.post("/{player_id}/characters")
def add_character(
    player_id: int,
    data: PlayerCharacterCreate,
    db: Session = Depends(get_database),
):
    # Check player exists
    player = db.query(Player).filter(
        Player.player_id == player_id
    ).first()

    if not player:
        raise HTTPException(
            status_code=404,
            detail="Player not found",
        )

    # Check character exists
    character = db.query(Character).filter(
        Character.character_id == data.character_id
    ).first()

    if not character:
        raise HTTPException(
            status_code=404,
            detail="Character not found",
        )

    # Check character isn't already added
    existing = db.query(PlayerCharacter).filter(
        PlayerCharacter.player_id == player_id,
        PlayerCharacter.character_id == data.character_id,
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Character already added to player",
        )

    # Validate friendship level
    if data.friendship_level < 0:
        raise HTTPException(
            status_code=400,
            detail="Friendship level cannot be negative",
        )

    if data.friendship_level > character.max_friendship_level:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Friendship level cannot exceed "
                f"{character.max_friendship_level}"
            ),
        )

    # Validate role if provided
    if data.role_id is not None:
        role = db.query(Role).filter(
            Role.role_id == data.role_id
        ).first()

        if not role:
            raise HTTPException(
                status_code=404,
                detail="Role not found",
            )

    player_character = PlayerCharacter(
        player_id=player_id,
        character_id=data.character_id,
        unlocked=data.unlocked,
        friendship_level=data.friendship_level,
        assigned_role=data.role_id,
    )

    try:
        db.add(player_character)
        db.commit()
        db.refresh(player_character)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to add character",
        )

    return {
        "message": "Character added",
        "character_id": player_character.character_id,
    }


@router.patch("/{player_id}/characters/{character_id}")
def update_character(
    player_id: int,
    character_id: int,
    data: PlayerCharacterUpdate,
    db: Session = Depends(get_database),
):
    # Find player's character
    player_character = db.query(PlayerCharacter).filter(
        PlayerCharacter.player_id == player_id,
        PlayerCharacter.character_id == character_id,
    ).first()

    if not player_character:
        raise HTTPException(
            status_code=404,
            detail="Character not found for this player",
        )

    # Validate friendship level if provided
    if data.friendship_level is not None:
        if data.friendship_level < 0:
            raise HTTPException(
                status_code=400,
                detail="Friendship level cannot be negative",
            )

        if data.friendship_level > player_character.character.max_friendship_level:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Friendship level cannot exceed "
                    f"{player_character.character.max_friendship_level}"
                ),
            )

        player_character.friendship_level = data.friendship_level

    # Update unlocked status if provided
    if data.unlocked is not None:
        player_character.unlocked = data.unlocked

    # Validate and update role if provided
    if data.role_id is not None:
        role = db.query(Role).filter(
            Role.role_id == data.role_id
        ).first()

        if not role:
            raise HTTPException(
                status_code=404,
                detail="Role not found",
            )

        player_character.assigned_role = data.role_id

    try:
        db.commit()
        db.refresh(player_character)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to update character",
        )

    return {
        "message": "Character updated",
        "character_id": player_character.character_id,
        "unlocked": player_character.unlocked,
        "friendship_level": player_character.friendship_level,
        "role_id": player_character.assigned_role,
    }
