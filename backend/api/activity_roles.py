from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.session import get_database
from backend.database.models import (
    Player,
    Role,
)

from backend.schemas.activity_roles import (
    ActivityRoleResponse,
    RoleCharacterResponse,
)


router = APIRouter(
    prefix="/players",
    tags=["activities & roles"],
)


@router.get(
    "/{player_id}/activities-roles",
    response_model=list[ActivityRoleResponse],
)
def get_activity_roles(
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

    roles = db.query(Role).order_by(
        Role.role_id
    ).all()

    results = []

    for role in roles:

        assigned_characters = [
            pc
            for pc in player.characters
            if (
                pc.role_status == "assigned"
                and pc.assigned_role == role.role_id
            )
        ]

        no_role_characters = [
            pc
            for pc in player.characters
            if pc.role_status == "no_role"
        ]

        unknown_characters = [
            pc
            for pc in player.characters
            if pc.role_status == "unknown"
        ]

        results.append(
            ActivityRoleResponse(
                role_id=role.role_id,
                role=role.name,
                assigned_count=len(assigned_characters),
                assigned_characters=[
                    RoleCharacterResponse(
                        name=pc.character.name,
                        friendship_level=pc.friendship_level,
                        unlocked=pc.unlocked,
                    )
                    for pc in assigned_characters
                ],
                no_role_count=len(no_role_characters),
                unknown_count=len(unknown_characters),
            )
        )

    return results