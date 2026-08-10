from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import (
    Character,
    PlayerCharacter,
)


def get_all_characters(session: Session) -> list[Character]:
    """Return all characters in the game."""

    statement = select(Character).order_by(Character.name)

    return list(session.scalars(statement).all())


def get_unlocked_characters(
    session: Session,
    player_id: int
) -> list[PlayerCharacter]:
    """Return all characters unlocked by a specific player."""

    statement = (
        select(PlayerCharacter)
        .where(
            PlayerCharacter.player_id == player_id,
            PlayerCharacter.unlocked.is_(True)
        )
        .order_by(PlayerCharacter.friendship_level.desc())
    )

    return list(session.scalars(statement).all())


def get_characters_by_role(
    session: Session,
    player_id: int,
    role_id: int
) -> list[PlayerCharacter]:
    """Return a player's characters assigned to a specific role."""

    statement = (
        select(PlayerCharacter)
        .where(
            PlayerCharacter.player_id == player_id,
            PlayerCharacter.assigned_role == role_id
        )
        .order_by(PlayerCharacter.friendship_level.desc())
    )

    return list(session.scalars(statement).all())