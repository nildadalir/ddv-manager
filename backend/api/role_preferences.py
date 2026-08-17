from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.session import get_database
from backend.database.models import (
    Player,
    Role,
    PlayerRolePreference,
)
from backend.schemas.role_preferences import (
    RolePreferenceResponse,
    RolePreferenceUpdate,
)


router = APIRouter(
    prefix="/players",
    tags=["role preferences"],
)


@router.get(
    "/{player_id}/role-preferences",
    response_model=list[RolePreferenceResponse],
)
def get_role_preferences(
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

    preferences = db.query(PlayerRolePreference).filter(
        PlayerRolePreference.player_id == player_id
    ).order_by(
        PlayerRolePreference.priority
    ).all()

    return [
        RolePreferenceResponse(
            role_id=preference.role_id,
            role=preference.role.name,
            priority=preference.priority,
        )
        for preference in preferences
    ]


@router.put(
    "/{player_id}/role-preferences",
    response_model=list[RolePreferenceResponse],
)
def update_role_preferences(
    player_id: int,
    data: RolePreferenceUpdate,
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

    roles = db.query(Role).all()

    role_ids = {role.role_id for role in roles}

    submitted_role_ids = {
        preference.role_id
        for preference in data.preferences
    }

    if submitted_role_ids != role_ids:
        raise HTTPException(
            status_code=400,
            detail="All roles must be included exactly once",
        )

    priorities = [
        preference.priority
        for preference in data.preferences
    ]

    if len(priorities) != len(set(priorities)):
        raise HTTPException(
            status_code=400,
            detail="Each role must have a unique priority",
        )

    db.query(PlayerRolePreference).filter(
        PlayerRolePreference.player_id == player_id
    ).delete()

    for preference in data.preferences:
        db.add(
            PlayerRolePreference(
                player_id=player_id,
                role_id=preference.role_id,
                priority=preference.priority,
            )
        )

    db.commit()

    preferences = db.query(PlayerRolePreference).filter(
        PlayerRolePreference.player_id == player_id
    ).order_by(
        PlayerRolePreference.priority
    ).all()

    return [
        RolePreferenceResponse(
            role_id=preference.role_id,
            role=preference.role.name,
            priority=preference.priority,
        )
        for preference in preferences
    ]