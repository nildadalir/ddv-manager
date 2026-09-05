from backend.database.models import PlayerUnlockSource


def set_player_unlock_source_state(
    player_id,
    unlock_source_id,
    unlocked,
    db,
):
    progress = (
        db.query(PlayerUnlockSource)
        .filter_by(
            player_id=player_id,
            unlock_source_id=unlock_source_id,
        )
        .first()
    )

    if progress is None:
        raise ValueError(
            "Player unlock source progress does not exist."
        )

    if unlocked not in (True, False, None):
        raise ValueError(
            "Unlock source state must be True, False, or None."
        )

    progress.unlocked = unlocked

    db.commit()

    return progress