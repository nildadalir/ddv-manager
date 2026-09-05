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
    PlayerPreferenceUpdate,
)

from backend.services.recommendation import (
    generate_player_recommendations,
)


router = APIRouter(
    prefix="/players",
    tags=["players"],
)


ALLOWED_ROLE_STATUSES = {
    "assigned",
    "no_role",
    "unknown",
}


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
                    role=(
                        pc.role.name
                        if pc.role_status == "assigned" and pc.role
                        else None
                    ),
                    role_status=pc.role_status,
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
        1
        for pc in characters
        if pc.unlocked is True
    )

    max_friendship_count = sum(
        1
        for pc in characters
        if (
            pc.friendship_level is not None
            and pc.friendship_level >= pc.character.max_friendship_level
        )
    )

    assigned_roles = [
        {
            "character": pc.character.name,
            "role": pc.role.name,
        }
        for pc in characters
        if pc.role_status == "assigned" and pc.role
    ]

    used_roles = {
        pc.role.name
        for pc in characters
        if pc.role_status == "assigned" and pc.role
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

    return generate_player_recommendations(
        player_id,
        player,
        db,
    )


@router.patch("/{player_id}/preferences")
def update_player_preferences(
    player_id: int,
    data: PlayerPreferenceUpdate,
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

    allowed_strategies = {
        "finish_closest",
        "lowest_level",
        "highest_level",
        "balanced",
        "custom",
    }

    if data.friendship_strategy not in allowed_strategies:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid friendship strategy. "
                f"Allowed values: {', '.join(allowed_strategies)}"
            ),
        )

    player.friendship_strategy = data.friendship_strategy

    db.commit()
    db.refresh(player)

    return {
        "message": "Player preferences updated",
        "friendship_strategy": player.friendship_strategy,
    }


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

    if data.friendship_level is not None:

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

    if data.role_status not in ALLOWED_ROLE_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid role status. "
                "Allowed values: assigned, no_role, unknown"
            ),
        )

    if data.role_status == "assigned":

        if data.role_id is None:
            raise HTTPException(
                status_code=400,
                detail="An assigned role requires a role_id",
            )

        role = db.query(Role).filter(
            Role.role_id == data.role_id
        ).first()

        if not role:
            raise HTTPException(
                status_code=404,
                detail="Role not found",
            )

    else:

        if data.role_id is not None:
            raise HTTPException(
                status_code=400,
                detail=(
                    "role_id must be null unless "
                    "role_status is assigned"
                ),
            )

    player_character = PlayerCharacter(
        player_id=player_id,
        character_id=data.character_id,
        unlocked=data.unlocked,
        friendship_level=data.friendship_level,
        assigned_role=data.role_id,
        role_status=data.role_status,
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

        if (
            data.friendship_level
            > player_character.character.max_friendship_level
        ):
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

    if data.role_status is not None:

        if data.role_status not in ALLOWED_ROLE_STATUSES:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid role status. "
                    "Allowed values: assigned, no_role, unknown"
                ),
            )

        if data.role_status == "assigned":

            if data.role_id is None:
                raise HTTPException(
                    status_code=400,
                    detail="An assigned role requires a role_id",
                )

            role = db.query(Role).filter(
                Role.role_id == data.role_id
            ).first()

            if not role:
                raise HTTPException(
                    status_code=404,
                    detail="Role not found",
                )

            player_character.assigned_role = data.role_id

        else:

            if data.role_id is not None:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "role_id must be null unless "
                        "role_status is assigned"
                    ),
                )

            player_character.assigned_role = None

        player_character.role_status = data.role_status

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
        "role_status": player_character.role_status,
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