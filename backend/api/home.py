from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.models import Player
from backend.database.session import get_database
from backend.services.home import generate_home_summary


router = APIRouter(
    prefix="/home",
    tags=["home"],
)


@router.get("/")
def get_home(
    db: Session = Depends(get_database),
):
    player = db.query(Player).first()

    if player is None:
        return {
            "error": "No player found"
        }

    return generate_home_summary(
        player_id=player.player_id,
        player=player,
        db=db,
    )