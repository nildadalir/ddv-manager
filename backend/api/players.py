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
    PlayerSummaryResponse,
    PlayerRecommendationResponse,
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


@router.get("/{player_id}/summary", response_model=PlayerSummaryResponse)
def get_player_summary(
    player_id: int,
    db: Session = Depends(get_database),
):
    player = db.query(Player).filter(
        Player.player_id == player_id
    ).first()

    if not player:
        raise HTTPException(
            status_code=404,
            detail="Player not found",
        )

    characters = player.characters

    unlocked_count = sum(
        1 for pc in characters if pc.unlocked
    )

    max_friendship_count = sum(
        1
        for pc in characters
        if pc.friendship_level >= pc.character.max_friendship_level
    )

    assigned_roles = [
        {
            "character": pc.character.name,
            "role": pc.role.name,
        }
        for pc in characters
        if pc.role
    ]

    used_roles = {
        pc.role.name
        for pc in characters
        if pc.role
    }

    all_roles = db.query(Role).all()

    missing_roles = [
        role.name
        for role in all_roles
        if role.name not in used_roles
    ]

    return PlayerSummaryResponse(
        username=player.username,
        total_characters=len(characters),
        unlocked_characters=unlocked_count,
        max_friendship_characters=max_friendship_count,
        assigned_roles=assigned_roles,
        missing_roles=missing_roles,
    )

@router.get(
    "/{player_id}/recommendations",
    response_model=list[PlayerRecommendationResponse],
)
def get_player_recommendations(
    player_id: int,
    db: Session = Depends(get_database),
):
    player = db.query(Player).filter(
        Player.player_id == player_id
    ).first()

    if not player:
        raise HTTPException(
            status_code=404,
            detail="Player not found",
        )

    recommendations = []

    # ---------- Friendship recommendations ----------
    for pc in player.characters:

        if pc.friendship_level >= pc.character.max_friendship_level:
            continue

        remaining = (
            pc.character.max_friendship_level
            - pc.friendship_level
        )

        if remaining <= 2:
            priority = "high"
            score = 100 - remaining

        elif remaining <= 6:
            priority = "medium"
            score = 60 - remaining

        else:
            priority = "low"
            score = 20 - remaining

        recommendations.append(
            {
                "type": "friendship",
                "priority": priority,
                "character": pc.character.name,
                "reason": (
                    f"Friendship level "
                    f"{pc.friendship_level}/"
                    f"{pc.character.max_friendship_level}"
                ),
                "score": score,
            }
        )

    # ---------- Missing role recommendations ----------
    role_priority = {
        "Gardening": ("high", 90),
        "Mining": ("high", 85),
        "Fishing": ("medium", 60),
        "Foraging": ("medium", 55),
        "Digging": ("low", 30),
    }

    assigned_roles = {
        pc.role.name
        for pc in player.characters
        if pc.role
    }

    for role in db.query(Role).all():

        if role.name in assigned_roles:
            continue

        priority, score = role_priority.get(
            role.name,
            ("medium", 50),
        )

        recommendations.append(
            {
                "type": "role",
                "priority": priority,
                "character": None,
                "reason": (
                    f"No character assigned to {role.name}"
                ),
                "score": score,
            }
        )

    # ---------- Sort by score ----------
    recommendations.sort(
        key=lambda r: r["score"],
        reverse=True,
    )

    # Remove internal score before returning
    for recommendation in recommendations:
        recommendation.pop("score")

    return recommendations

@router.post("/{player_id}/characters")
def add_character(
    player_id: int,
    data: PlayerCharacterCreate,
    db: Session = Depends(get_database),
):
    player = db.query(Player).filter(
        Player.player_id == player_id
    ).first()

    if not player:
        raise HTTPException(
            status_code=404,
            detail="Player not found",
        )

    character = db.query(Character).filter(
        Character.character_id == data.character_id
    ).first()

    if not character:
        raise HTTPException(
            status_code=404,
            detail="Character not found",
        )

    existing = db.query(PlayerCharacter).filter(
        PlayerCharacter.player_id == player_id,
        PlayerCharacter.character_id == data.character_id,
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Character already added to player",
        )

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
    player_character = db.query(PlayerCharacter).filter(
        PlayerCharacter.player_id == player_id,
        PlayerCharacter.character_id == character_id,
    ).first()

    if not player_character:
        raise HTTPException(
            status_code=404,
            detail="Character not found for this player",
        )

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

    if data.unlocked is not None:
        player_character.unlocked = data.unlocked

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


@router.delete("/{player_id}/characters/{character_id}")
def remove_character(
    player_id: int,
    character_id: int,
    db: Session = Depends(get_database),
):
    player_character = db.query(PlayerCharacter).filter(
        PlayerCharacter.player_id == player_id,
        PlayerCharacter.character_id == character_id,
    ).first()

    if not player_character:
        raise HTTPException(
            status_code=404,
            detail="Character not found for this player",
        )

    db.delete(player_character)
    db.commit()

    return {
        "message": "Character removed",
        "character_id": character_id,
    }