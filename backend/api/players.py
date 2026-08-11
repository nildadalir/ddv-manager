from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.session import get_database
from backend.database.models import Player

from backend.schemas.player import (
    PlayerResponse,
    PlayerCharacterResponse
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